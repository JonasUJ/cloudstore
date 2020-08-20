from rest_framework import serializers

from ..models import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'files', 'folders', 'parent', 'owner']
        extra_kwargs = {
            'parent': {'allow_null': False},
            'files': {'read_only': True},
            'folders': {'read_only': True},
            'owner': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request']
        self.fields['parent'].queryset = self.fields['parent'].queryset.filter(owner=request.user)
        super().__init__(*args, **kwargs)

    def validate_parent(self, parent):
        pk = self.context.get('pk', False)

        # pk it not passed when creating folders
        if not pk:
            return parent

        folder = Folder.objects.get(pk=pk)
        if parent == folder:
            raise serializers.ValidationError('Folder cannot be its own parent')
        if folder.deep_contains(parent):
            raise serializers.ValidationError('Folder cannot contain its own parent')
        return parent
