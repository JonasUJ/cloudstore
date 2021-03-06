from rest_framework import serializers

from sanitize_filename import sanitize

from . import FileSerializer
from ..models import File, Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'uuid', 'files', 'folders', 'folder', 'owner']
        extra_kwargs = {
            'folder': {'allow_null': False},
            'files': {'read_only': True},
            'folders': {'read_only': True},
            'owner': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request']
        self.fields['folder'].queryset = self.fields['folder'].queryset.filter(owner=request.user)
        super().__init__(*args, **kwargs)
        self.context['data'] = kwargs.get('data')

    def validate_name(self, name):
        parent = self.context['data']['folder']

        if (
            Folder.objects.filter(folder=parent, name=name).exists()
            or File.objects.filter(folder=parent, name=name).exists()
        ):
            i = 2
            new_name = f'{name} ({i})'
            while (
                Folder.objects.filter(folder=parent, name=new_name).exists()
                or File.objects.filter(folder=parent, name=new_name).exists()
            ):
                i += 1
                new_name = f'{name} ({i})'
            name = new_name

        return sanitize(name)

    def validate_folder(self, folder):
        folder_pk = self.context.get('pk', False)

        # pk it not passed when creating folders
        if not folder_pk:
            return folder

        _folder = Folder.objects.get(pk=folder_pk)
        if folder == _folder:
            raise serializers.ValidationError('Folder cannot be its own parent')
        if folder.deep_contains(folder):
            raise serializers.ValidationError('Folder cannot contain its own parent')
        return folder


class FolderContentsSerializer(FolderSerializer):
    files = serializers.SerializerMethodField()
    folders = serializers.SerializerMethodField()

    def get_files(self, obj):
        return [
            FileSerializer(o, context=self.context).data for o in File.objects.filter(folder=obj.pk)
        ]

    def get_folders(self, obj):
        return [
            FolderSerializer(o, context=self.context).data
            for o in Folder.objects.filter(folder=obj.pk)
        ]
