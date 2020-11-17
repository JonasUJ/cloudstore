from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views import View

from cloudstore.apps.api.models import Folder  # noqa pylint: disable=import-error


class FolderZipView(View):
    def get(self, request: HttpRequest, uuid='') -> HttpResponse:
        try:
            folder = Folder.objects.get(uuid=uuid)
        except Folder.DoesNotExistError:
            raise PermissionDenied()

        # NOTE: Implement sharing folders here eventually.
        # Something equivalent to PrivateFile.can_access_file.
        if not (request.user.is_authenticated and request.user == folder.owner):
            raise PermissionDenied()

        temp = folder.temp_zip()
        temp.seek(0)

        if settings.DEBUG:
            response = FileResponse(temp, as_attachment=True, filename=f'{folder.name}.zip')
        else:
            response = HttpResponse()

            # This assumes NGINX, which is also what we are using.
            response['X-Accel-Redirect'] = temp.name
            response['Content-Length'] = temp.tell()
            response['Content-Type'] = 'application/octet-stream'

        return response
