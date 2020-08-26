from django.db import IntegrityError

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..models import Folder
from ..permissions import IsSelf
from ..serializers import FolderContentsSerializer, FolderSerializer


class FolderViewSet(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated, IsSelf]

    def perform_create(self, serializer: FolderSerializer):
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except IntegrityError:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        folder_pk = self.kwargs.get('pk', False)
        if folder_pk:
            try:
                context['pk'] = int(folder_pk)
            except ValueError:
                pass
        return context


class FolderContentsView(RetrieveAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderContentsSerializer
    permission_classes = [IsAuthenticated, IsSelf]
