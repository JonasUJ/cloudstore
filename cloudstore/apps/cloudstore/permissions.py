# Only accepts CloudstorePrivateFile, but it cannot be typehinted due to circular dependency
def allow_owner(private_file) -> bool:
    return private_file.request.user == private_file.file.get().owner
