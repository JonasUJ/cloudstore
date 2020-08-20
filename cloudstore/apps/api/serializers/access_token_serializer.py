from rest_framework.serializers import ModelSerializer  # pylint: disable=import-error

from ..models import AccessToken


class AccessTokenSerializer(ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ['token']
