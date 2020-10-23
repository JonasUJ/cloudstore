import mimetypes

from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property
from django.utils.html import escape
from django.views.generic import FormView

from private_storage.models import PrivateFile
from private_storage.views import PrivateStorageView

from cloudstore.apps.api.models import ShareState  # noqa pylint: disable=import-error

from ..forms import ResourcePasswordForm
from ...api.models import File


class CloudstorePrivateFile(PrivateFile):
    def __init__(self, *args, thumb=False, **kwargs):
        self.thumb = thumb
        super().__init__(*args, **kwargs)
        self.file = File.objects.filter(uuid=self.relative_name)

    @cached_property
    def name(self):
        if self.thumb:
            return self.file.get().thumb.name
        return self.file.get().file.name

    @cached_property
    def full_path(self):
        return self.storage.path(self.name)

    def open(self, mode='rb'):
        file = self.storage.open(self.name, mode=mode)
        return file

    def exists(self):
        return self.relative_name and self.storage.exists(self.relative_name) and self.file.exists()

    @cached_property
    def content_type(self):
        filename = self.file.get().name
        mimetype, encoding = mimetypes.guess_type(filename)  # pylint: disable=unused-variable
        return mimetype or 'application/octet-stream'


def get_form_view(file, form):
    return FormView.as_view(
        form_class=form,
        template_name='misc/resource_password.html',
        extra_context={
            'title': 'Password required',
            'content': f'The file <code>{escape(file.name)}</code> has been password '
            'protected by its owner.',
        },
    )


class CloudstorePrivateStorageView(PrivateStorageView):
    content_disposition = 'inline'
    thumb = False

    def get_private_file(self):
        return CloudstorePrivateFile(
            thumb=self.thumb,
            request=self.request,
            storage=self.get_storage(),
            relative_name=self.get_path(),
        )

    def get_content_disposition_filename(self, private_file):
        return self.content_disposition_filename or private_file.file.get().name

    def get(self, request, *args, **kwargs):
        private_file = self.get_private_file()

        if not self.can_access_file(private_file):
            raise PermissionDenied(self.permission_denied_message)

        file = private_file.file.get()
        if (
            file.share.state == ShareState.PASSWORD_PROTECTED
            and file.owner != private_file.request.user
        ):
            password_view = get_form_view(
                file, lambda *args, **kwargs: ResourcePasswordForm(file, *args, **kwargs)
            )
            return password_view(private_file.request)

        return self.serve_file(private_file)

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        private_file = self.get_private_file()

        if not self.can_access_file(private_file):
            raise PermissionDenied(self.permission_denied_message)

        form = ResourcePasswordForm(private_file.file.get(), request.POST)
        if form.is_valid():
            return self.serve_file(private_file)

        password_view = get_form_view(private_file.file.get(), lambda *args, **kwargs: form)
        return password_view(private_file.request)
