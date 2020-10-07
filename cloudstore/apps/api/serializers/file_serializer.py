import os.path

from rest_framework import serializers

from ..models import File, Folder


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            'id',
            'name',
            'file',
            'size',
            'thumb',
            'folder',
            'owner',
            'created',
            'accessed',
            'clean_name',
            'ext',
        ]
        extra_kwargs = {
            'thumb': {'read_only': True},
            'owner': {'read_only': True},
            'file': {'allow_empty_file': True},
        }

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request']
        self.fields['folder'].queryset = self.fields['folder'].queryset.filter(owner=request.user)

        if request.method in ('PUT', 'PATCH'):
            self.fields['file'].read_only = True
            self.fields['file'].required = False
            self.fields['folder'].required = False
        super().__init__(*args, **kwargs)
        self.context['data'] = kwargs.get('data')

    def validate(self, attrs):
        if 'file' in attrs:
            attrs['size'] = attrs['file'].size
        return attrs

    def validate_file(self, file):
        user = self.context['request'].user
        user.quota.refresh_from_db()

        if file.size + user.quota.used > user.quota.allowed:
            raise serializers.ValidationError('File size exceeds user quota')

        user.quota.use(file.size)
        return file

    def validate_name(self, name):
        parent = self.context['data']['folder']

        if (
            Folder.objects.filter(folder=parent, name=name).exists()
            or File.objects.filter(folder=parent, name=name).exists()
        ):
            i = 2
            base, ext = os.path.splitext(name)
            new_name = f'{base} ({i}){ext}'
            while (
                Folder.objects.filter(folder=parent, name=new_name).exists()
                or File.objects.filter(folder=parent, name=new_name).exists()
            ):
                i += 1
                new_name = f'{base} ({i}){ext}'
            name = new_name

        return name
