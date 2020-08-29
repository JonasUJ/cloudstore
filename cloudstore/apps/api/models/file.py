import os
from io import BytesIO

from PIL import Image, UnidentifiedImageError

from django.conf import settings
from django.core.files import File as CoreFile
from django.db import models
from django.dispatch import receiver

from private_storage.fields import PrivateFileField

from shortuuid import uuid


def get_uuid() -> str:
    return uuid()[:8]


def get_filename(instance, filename) -> str:  # pylint: disable=unused-argument
    return f'{instance.uuid}'


def get_thumbnail_filename(instance, filename) -> str:  # pylint: disable=unused-argument
    return f'thumb/{get_filename(instance, filename)}'


class NotRequiredPrivateFileField(PrivateFileField):
    """See https://code.djangoproject.com/ticket/13327"""

    def _require_file(self):
        return

    @property
    def url(self):
        if self:
            return self.storage.url(self.name)
        return ''


class File(models.Model):
    name = models.CharField(max_length=200)
    uuid = models.CharField(max_length=8, default=get_uuid, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    accessed = models.DateTimeField(auto_now=True)
    file = PrivateFileField(upload_to=get_filename)
    thumb = NotRequiredPrivateFileField(upload_to=get_thumbnail_filename, blank=True, null=True)
    folder = models.ForeignKey('Folder', related_name='files', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='files',
                              on_delete=models.CASCADE)

    def ext(self) -> str:
        return os.path.splitext(self.name)[1]

    def clean_name(self) -> str:
        return os.path.splitext(self.name)[0]

    def generate_thumbnail(self):
        ext = self.ext().strip('.').upper()
        if ext == 'JPG':
            ext = 'JPEG'

        if ext in settings.IMAGE_THUMBNAIL_TYPES:
            try:
                img = Image.open(self.file.file)
                img.thumbnail(settings.IMAGE_THUMBNAIL_SIZE)
                img_bytes = BytesIO()
                img.save(img_bytes, format=ext)
                self.thumb.save(self.thumb.name, CoreFile(img_bytes))
            except UnidentifiedImageError:
                pass  # We couldn't open the image, probably because it isn't one.

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=File)
def remove_file(sender, instance: File, **kwargs):  # pylint: disable=unused-argument
    instance.file.delete(False)
    instance.thumb.delete(False)
