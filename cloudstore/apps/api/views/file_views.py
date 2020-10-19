from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..models import File, Share
from ..permissions import IsSelf
from ..serializers import FileSerializer, ShareSerializer


class ShareRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(file__owner=self.request.user)


class FileViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def perform_create(self, serializer: FileSerializer):
        file = serializer.save(owner=self.request.user)
        file.generate_thumbnail()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
