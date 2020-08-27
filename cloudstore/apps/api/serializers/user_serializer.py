from django.contrib.auth import get_user_model

from rest_framework import serializers

from ...cloudstore.models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'files', 'folders', 'base_folder', 'settings']
        extra_kwargs = {
            'files': {'read_only': True},
            'folders': {'read_only': True},
            'base_folder': {'read_only': True},
        }

    settings = serializers.SerializerMethodField()

    def get_settings(self, obj):
        return UserSettingsSerializer(
            UserSettings.objects.get(pk=obj.pk),
            context=self.context
        ).data
