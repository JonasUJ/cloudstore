from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'files', 'folders', 'base_folder']
        extra_kwargs = {
            'files': {'read_only': True},
            'folders': {'read_only': True},
            'base_folder': {'read_only': True},
        }
