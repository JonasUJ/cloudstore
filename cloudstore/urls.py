from django.conf.urls import include as conf_include
from django.contrib import admin
from django.urls import include, path, re_path

from cloudstore.apps.cloudstore.views import PrivateStorageView  # noqa pylint: disable=import-error


urlpatterns = [
    path('', include('cloudstore.apps.cloudstore.urls', namespace='cloudstore')),
    path('api/', include('cloudstore.apps.api.urls', namespace='api')),
    re_path(
        '^m/thumb/(?P<path>.*)$',
        PrivateStorageView.as_view(thumb=True),
        name='serve_private_file_thumb',
    ),
    re_path('^m/(?P<path>.*)$', PrivateStorageView.as_view(), name='serve_private_file'),
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', conf_include('rest_framework.urls')),
]
