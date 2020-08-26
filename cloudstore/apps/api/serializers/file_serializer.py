from rest_framework import serializers

from ..models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'folder', 'owner',
                  'created', 'accessed', 'clean_name', 'ext']
        extra_kwargs = {
            'owner': {'read_only': True},
        }

    def __init__(self, *args, **kwargs):
        request = kwargs['context']['request']
        self.fields['folder'].queryset = self.fields['folder'].queryset.filter(owner=request.user)

        if request.method in ('PUT', 'PATCH'):
            self.fields['file'].read_only = True
            self.fields['file'].required = False
            self.fields['folder'].required = False
        super().__init__(*args, **kwargs)
