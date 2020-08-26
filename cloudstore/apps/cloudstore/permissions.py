from django.core.exceptions import ObjectDoesNotExist


# Only accepts CloudstorePrivateFile, but it cannot be typehinted due to circular dependency
def allow_owner(private_file) -> bool:
    try:
        return private_file.request.user == private_file.file.get().owner
    except ObjectDoesNotExist:
        return False
