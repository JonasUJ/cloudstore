from django.conf import settings
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from .forms import (
    CloudstorePasswordResetForm,
    CloudstoreSetPasswordForm,
)
from .views import (
    AccountView,
    HomeView,
    LoginView,
    SignUpView,
)

app_name = 'cloudstore'
urlpatterns = [
    # General
    path('', HomeView.as_view(), name='home'),
    path('contact/', HomeView.as_view(), name='contact'),
    # Account
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('account/', AccountView.as_view(), name='account'),
    path(
        'account/password_reset/',
        PasswordResetView.as_view(
            form_class=CloudstorePasswordResetForm,
            template_name='account/reset_password.html',
            email_template_name='account/reset_password_email.html',
            success_url=reverse_lazy('cloudstore:password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'account/password_reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            form_class=CloudstoreSetPasswordForm,
            template_name='account/set_password.html',
            success_url=reverse_lazy('cloudstore:password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'account/password_reset/done/',
        TemplateView.as_view(
            template_name='base/blank.html',
            extra_context={
                'title': 'Email sent',
                'heading': 'Password reset e-mail sent',
                # NOTE: Can't use reverse() for "/login" here
                'content': 'An e-mail has been sent to your e-mail address '
                'with instructions on how to reset your password. '
                '<a href="/login">Sign in <i class="fas fa-arrow-right"></i></a>',
            },
        ),
        name='password_reset_done',
    ),
    path(
        'account/password_reset/complete/',
        TemplateView.as_view(
            template_name='base/blank.html',
            extra_context={
                'title': 'Password reset',
                'heading': 'Your password has been reset',
                # NOTE: Can't use reverse() for "/login" here
                'content': '<a href="/login">Sign in <i class="fas fa-arrow-right"></i></a>',
            },
        ),
        name='password_reset_complete',
    ),
]
