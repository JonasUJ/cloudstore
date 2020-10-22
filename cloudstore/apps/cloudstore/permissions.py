from django.core.exceptions import ObjectDoesNotExist

from cloudstore.apps.api.models import ShareState  # noqa pylint: disable=import-error


# Only accepts CloudstorePrivateFile, but it cannot be typehinted due to circular dependency
def allow_owner(private_file) -> bool:
    try:
        return private_file.request.user == private_file.file.get().owner
    except ObjectDoesNotExist:
        return False


def if_shared(private_file) -> bool:
    try:
        share = private_file.file.get().share
    except ObjectDoesNotExist:
        return False
    return share.state in (ShareState.PUBLIC, ShareState.PASSWORD_PROTECTED) or allow_owner(
        private_file
    )
