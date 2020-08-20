import os

from django.conf import settings
from django.db import models
from django.dispatch import receiver

from private_storage.fields import PrivateFileField

from shortuuid import uuid


def get_uuid():
    return uuid()[:8]


def get_filename(instance, filename):  # pylint: disable=unused-argument
    return f'{instance.uuid}'


class File(models.Model):
    name = models.CharField(max_length=200)
    uuid = models.CharField(max_length=8, default=get_uuid, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    accessed = models.DateTimeField(auto_now=True)
    file = PrivateFileField(upload_to=get_filename)
    folder = models.ForeignKey('Folder', related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='files',
                              on_delete=models.CASCADE)

    def ext(self):
        return os.path.splitext(self.name)[1]

    def clean_name(self):
        return os.path.splitext(self.name)[0]

    def __str__(self):
        return self.name


@receiver(models.signals.pre_delete, sender=File)
def remove_file(sender, instance: File, using, **kwargs):  # pylint: disable=unused-argument
    instance.file.delete()
