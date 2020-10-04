from django.contrib.auth import get_user_model

from rest_framework import serializers

from ...cloudstore.models import UserQuota, UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ['id', 'user']


class UserQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuota
        exclude = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'files', 'folders', 'base_folder', 'settings', 'quota']
        extra_kwargs = {
            'files': {'read_only': True},
            'folders': {'read_only': True},
            'base_folder': {'read_only': True},
        }

    settings = serializers.SerializerMethodField()
    quota = serializers.SerializerMethodField()

    def get_settings(self, user):
        return UserSettingsSerializer(user.settings, context=self.context).data

    def get_quota(self, user):
        return UserQuotaSerializer(user.quota, context=self.context).data
