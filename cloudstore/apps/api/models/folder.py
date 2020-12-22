import zipfile
from os.path import join
from tempfile import NamedTemporaryFile
from typing import Generator, Tuple, Union

from django.conf import settings
from django.db import models

from shortuuid import uuid

from ..models import File


def get_uuid() -> str:
    return uuid()[:8]


class Folder(models.Model):
    name = models.CharField(max_length=200)
    uuid = models.CharField(max_length=8, default=get_uuid, unique=True)
    folder = models.ForeignKey(
        'Folder', blank=True, null=True, related_name='folders', on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='folders', on_delete=models.CASCADE
    )

    def deep_contains(self, other: Union[File, 'Folder']) -> bool:
        """BFS for a File or Folder."""
        # pylint: disable=no-member
        if isinstance(other, Folder) and any(other.pk == f.pk for f in self.folders.all()):
            return True
        if isinstance(other, File) and any(other.pk == f.pk for f in self.files.all()):
            return True
        for folder in self.folders.all():
            if folder.deep_contains(other):
                return True
        return False

    def get_file_paths(self) -> Generator[Tuple[str, str], None, None]:
        """Generate 2-tuples with full name and relative names of all content."""
        # pylint: disable=no-member
        for file in self.files.all():
            yield join(settings.PRIVATE_STORAGE_ROOT, file.uuid), file.name

        # pylint: disable=no-member
        for folder in self.folders.all():
            for fullname, name in folder.get_file_paths():
                yield fullname, join(folder.name, name)

    def temp_zip(self) -> NamedTemporaryFile:
        """Zip all folder contents into a ZipFile and return it as a NamedTemporaryFile."""
        tempf = NamedTemporaryFile('r+b')
        zipf = zipfile.ZipFile(tempf, 'w', zipfile.ZIP_DEFLATED)
        for name, arcname in self.get_file_paths():
            zipf.write(name, arcname)
        # Why does tempf.seek(0) not work here, but it does right after the calling the function?
        return tempf

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
        if self.folder and self.folder.folder:
            return f'{self.folder.name}/{self.name}'
        return self.name
