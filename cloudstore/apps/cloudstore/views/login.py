from django.conf import settings
from django.contrib.auth.views import LoginView
from django.http import HttpRequest

from ..forms import LoginForm


class CloudstoreLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = LoginForm

    def post(self, request: HttpRequest, *args, **kwargs):
        if request.POST.get('remember_me', False):
            request.session.set_expiry(settings.SESSION_COOKIE_AGE)
        else:
            request.session.set_expiry(0)
        return super().post(request, *args, **kwargs)
