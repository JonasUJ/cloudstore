from django.conf.urls import include as conf_include
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path, re_path

from cloudstore.apps.cloudstore.views import (  # noqa pylint: disable=import-error
    FolderZipView,
    PrivateStorageView,
)


urlpatterns = [
    path('', include('cloudstore.apps.cloudstore.urls', namespace='cloudstore')),
    path('api/', include('cloudstore.apps.api.urls', namespace='api')),
    re_path(
        '^m/thumb/(?P<path>.*)$',
        PrivateStorageView.as_view(thumb=True),
        name='serve_private_file_thumb',
    ),
    re_path('^m/(?P<path>.*)$', PrivateStorageView.as_view(), name='serve_private_file'),
    re_path('^d/(?P<uuid>.*)$', FolderZipView.as_view(), name='serve_private_folder'),
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', conf_include('rest_framework.urls')),
]


def handler400(
    request, exception, template_name='base/error.html'
):  # pylint: disable=unused-argument
    return render(
        request,
        template_name,
        status=400,
        context={
            'error': 400,
            'heading': 'Error 400 - Bad Request',
            'content': 'Something about your request went wrong.',
        },
    )


def handler403(
    request, exception, template_name='base/error.html'
):  # pylint: disable=unused-argument
    return render(
        request,
        template_name,
        status=403,
        context={
            'error': 403,
            'heading': 'Error 403 - Permission denied',
            'content': 'You do not have permission to view this resource.',
        },
    )


def handler404(
    request, exception, template_name='base/error.html'
):  # pylint: disable=unused-argument
    return render(
        request,
        template_name,
        status=404,
        context={
            'error': 404,
            'heading': 'Error 404 - Page not found',
            'content': 'This page does not exist.',
        },
    )


def handler500(request, template_name='base/error.html'):
    return render(
        request,
        template_name,
        status=500,
        context={
            'error': 500,
            'heading': 'Error 500 - Internal server error',
            # NOTE: Not using reverse() for contact page
            'content': 'Woops, something went wrong. <a href="/contact">Contact</a> us and tell us '
            'what caused this.',
        },
    )
