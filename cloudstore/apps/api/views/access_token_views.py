from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser

from ..models import AccessToken
from ..serializers import AccessTokenSerializer


class AccessTokenCreate(CreateAPIView):
    queryset = AccessToken.objects.all()
    serializer_class = AccessTokenSerializer
    permission_classes = [IsAdminUser]
