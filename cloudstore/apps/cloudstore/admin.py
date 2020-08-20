from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CloudstoreUser


admin.site.register(CloudstoreUser, UserAdmin)
