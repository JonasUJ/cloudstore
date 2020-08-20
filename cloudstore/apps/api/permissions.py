from django.contrib.auth import get_user_model

from rest_framework import permissions

from . import models

User = get_user_model()


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        if isinstance(obj, (models.File, models.Folder)):
            return obj.owner == request.user
        return False
