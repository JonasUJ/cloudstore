from django.conf import settings
from django.db import models

from ..models import File


class Folder(models.Model):
    name = models.CharField(max_length=200)
    folder = models.ForeignKey(
        'Folder', blank=True, null=True, related_name='folders', on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='folders', on_delete=models.CASCADE
    )

    def deep_contains(self, other):
        """
        BFS for a File or Folder
        """
        # pylint: disable=no-member
        if isinstance(other, Folder) and any(other.pk == f.pk for f in self.folders.all()):
            return True
        if isinstance(other, File) and any(other.pk == f.pk for f in self.files.all()):
            return True
        for folder in self.folders.all():
            if folder.deep_contains(other):
                return True
        return False

    def __contains__(self, other):
        seq = []
        # pylint: disable=no-member
        if isinstance(other, Folder):
            seq = self.folders.all()
        elif isinstance(other, File):
            seq = self.files.all()
        else:
            raise ValueError(f'{other} is not a File or Folder')
        return any(other.pk == item.pk for item in seq)

    def __str__(self):
        return self.name
