import os.path

from rest_framework import serializers

from ..models import File, Folder
from ...cloudstore.models import UserQuota


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

    def validate_file(self, file):
        # Multiple requests may come in before any are handled.
        # We have to lock the quota and then get the latest from the DB
        # because it may have updated during handling of another request
        self.context['request'].user.quota.lock.acquire()
        quota = UserQuota.objects.get(pk=self.context['request'].user.quota.pk)
        try:
            if file.size + quota.used > quota.allowed:
                raise serializers.ValidationError('File size exceeds user quota')

            quota.use(file.size)
        finally:
            quota.lock.release()
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
