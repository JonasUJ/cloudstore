from rest_framework import serializers

from ..models import File, Folder


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'size', 'thumb', 'folder',
                  'owner', 'created', 'accessed', 'clean_name', 'ext']
        extra_kwargs = {
            'thumb': {'read_only': True},
            'owner': {'read_only': True},
            'file': {'allow_empty_file': True}
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

    def validate_name(self, name):
        parent = self.context['data']['folder']

        if Folder.objects.filter(folder=parent, name=name).exists() or \
           File.objects.filter(folder=parent, name=name).exists():
            raise serializers.ValidationError(
                'File cannot have the same name as an item in its parent'
            )

        return name
