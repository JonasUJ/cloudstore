from django.contrib.messages.views import SuccessMessageMixin
from django.forms import BaseForm
from django.http import HttpResponse
from django.shortcuts import reverse
from django.views.generic.edit import FormView


from cloudstore.apps.api.models import AccessToken  # noqa pylint: disable=import-error

from ..forms import SignUpForm


class SignUpView(SuccessMessageMixin, FormView):
    template_name = 'account/signup.html'
    form_class = SignUpForm
    success_message = 'Account created successfully. ' \
                      '<a href="{login}">Sign in <i class="fas fa-arrow-right"></i></a>'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(login=reverse('cloudstore:login'))

    def get_success_url(self):
        return reverse('cloudstore:signup')

    def form_valid(self, form: BaseForm) -> HttpResponse:
        AccessToken.objects.filter(token=form.cleaned_data['access_token']).delete()
        form.save()
        return super().form_valid(form)
