from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import File
from ..permissions import IsSelf
from ..serializers import FileSerializer


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def perform_create(self, serializer: FileSerializer):
        file = serializer.save(owner=self.request.user)
        file.generate_thumbnail()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
