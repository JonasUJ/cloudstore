from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from ..forms import CloudstorePasswordChangeForm, UserEditForm, UserSettingsForm


class AccountView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form_settings = UserSettingsForm(instance=request.user.settings, prefix='form_settings')
        form_user = UserEditForm(
            prefix='form_user',
            initial={'username': request.user.username, 'email': request.user.email},
        )
        form_password = CloudstorePasswordChangeForm(request.user, prefix='form_password')
        return render(
            request,
            'account/account.html',
            {
                'form_settings': form_settings,
                'form_user': form_user,
                'form_password': form_password,
            },
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form_settings = UserSettingsForm(
            request.POST, instance=request.user.settings, prefix='form_settings'
        )
        form_user = UserEditForm(request.POST, instance=request.user, prefix='form_user')
        form_password = CloudstorePasswordChangeForm(
            request.user, data=request.POST, prefix='form_password'
        )

        if any('form_settings' in k for k in request.POST):
            form_user = UserEditForm(
                prefix='form_user',
                initial={'username': request.user.username, 'email': request.user.email},
            )
            form_password = CloudstorePasswordChangeForm(request.user, prefix='form_password')

            if form_settings.is_valid():
                form_settings.save()

        elif any('form_user' in k for k in request.POST):
            form_settings = UserSettingsForm(instance=request.user.settings, prefix='form_settings')
            form_password = CloudstorePasswordChangeForm(request.user, prefix='form_password')
            if form_user.is_valid():
                form_user.save()

        elif any('form_password' in k for k in request.POST):
            form_settings = UserSettingsForm(instance=request.user.settings, prefix='form_settings')
            form_user = UserEditForm(
                prefix='form_user',
                initial={'username': request.user.username, 'email': request.user.email},
            )
            if form_password.is_valid():
                form_password.save()
                login(request, user=request.user)
                messages.success(request, 'Your password has been changed', 'form_password')

        return render(
            request,
            'account/account.html',
            {
                'form_settings': form_settings,
                'form_user': form_user,
                'form_password': form_password,
            },
        )
