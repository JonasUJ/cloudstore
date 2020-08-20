from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ..permissions import IsSelf
from ..serializers import UserSerializer


class UserRetrieveDestroyView(RetrieveDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelf]
