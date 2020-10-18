import os
from io import BytesIO
from mimetypes import guess_type

from PIL import Image, UnidentifiedImageError

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.files import File as CoreFile
from django.db import models
from django.dispatch import receiver

from private_storage.fields import PrivateFileField

from shortuuid import uuid


class ShareState(models.IntegerChoices):
    PRIVATE = 0
    PUBLIC = 1
    PASSWORD_PROTECTED = 2


class Share(models.Model):
    state = models.IntegerField(choices=ShareState.choices, default=ShareState.PRIVATE)
    key = models.CharField(max_length=100, blank=True, null=True)

    def matches(self, key):
        return check_password(key, self.key)

    def set_key(self, key):
        self.key = make_password(key)
        self.save()


def _get_share() -> Share:
    return Share.objects.create().pk


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
    size = models.BigIntegerField(default=0)
    thumb = NotRequiredPrivateFileField(upload_to=get_thumbnail_filename, blank=True, null=True)
    folder = models.ForeignKey('Folder', related_name='files', on_delete=models.CASCADE)
    share = models.OneToOneField(Share, on_delete=models.CASCADE, default=_get_share)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='files', on_delete=models.CASCADE
    )

    def ext(self) -> str:
        return os.path.splitext(self.name)[1]

    def clean_name(self) -> str:
        return os.path.splitext(self.name)[0]

    def text(self) -> bool:
        mimetype = guess_type(self.name)[0]
        if mimetype:
            mimetype = mimetype.split('/')[0] == 'text'
        return mimetype

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

                # NOTE: Thumbs can currently exceed the quota
                self.size += self.thumb.file.size
                self.save()
                self.owner.quota.use(self.thumb.file.size)
            except UnidentifiedImageError:
                pass  # We couldn't open the image, probably because it isn't one.

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=File)
def remove_file(sender, instance: File, **kwargs):  # pylint: disable=unused-argument
    instance.owner.quota.free(instance.size)
    instance.file.delete(False)
    instance.thumb.delete(False)
