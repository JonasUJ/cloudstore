from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CloudstoreUser, UserQuota


admin.site.register(CloudstoreUser, UserAdmin)


@admin.register(UserQuota)
class UserQuotaAdmin(admin.ModelAdmin):
    fields = ('allowed',)
