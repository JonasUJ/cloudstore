import mimetypes

from django.utils.functional import cached_property

from private_storage.models import PrivateFile
from private_storage.views import PrivateStorageView

from ...api.models import File


class CloudstorePrivateFile(PrivateFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = File.objects.filter(uuid=self.relative_name)

    def exists(self):
        return self.relative_name and \
            self.storage.exists(self.relative_name) and \
            self.file.exists()

    @cached_property
    def content_type(self):
        filename = self.file.get().name
        mimetype, encoding = mimetypes.guess_type(filename)  # pylint: disable=unused-variable
        return mimetype or 'application/octet-stream'


class CloudstorePrivateStorageView(PrivateStorageView):
    content_disposition = 'inline'

    def get_private_file(self):
        return CloudstorePrivateFile(
            request=self.request,
            storage=self.get_storage(),
            relative_name=self.get_path()
        )

    def get_content_disposition_filename(self, private_file):
        return self.content_disposition_filename or private_file.file.get().name
