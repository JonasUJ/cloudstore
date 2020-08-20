from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.forms import CharField, EmailField, PasswordInput, TextInput, ValidationError

from cloudstore.apps.api.models import AccessToken  # noqa pylint: disable=import-error

from .bulma_mixin import BulmaMixin


class SignUpForm(BulmaMixin, UserCreationForm):

    username = UsernameField(
        label='Username',
        max_length=25,
        widget=TextInput(
            attrs={'autofocus': True,
                   'autocomplete': 'username',
                   'class': 'has-background-black-bis'}),
    )
    email = EmailField(
        label='E-mail address',
        widget=TextInput(
            attrs={'autocomplete': 'email',
                   'class': 'has-background-black-bis'}),
        help_text='Used for password resets',
    )
    password1 = CharField(
        label='Password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'class': 'has-background-black-bis'}),
    )
    password2 = CharField(
        label='Confirm password',
        widget=PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'class': 'has-background-black-bis'}),
        strip=False,
        help_text='Enter the same password as before, for verification.',
    )
    access_token = CharField(
        label='Access token',
        widget=TextInput(attrs={'class': 'has-background-black-bis'}),
        help_text='An access token provided to you by the site administrator',
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'access_token')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields()
        self.add_attrs('username', {'icon_left': 'fa-user', 'is_horizontal': True})
        self.add_attrs('email', {'icon_left': 'fa-envelope', 'is_horizontal': True})
        self.add_attrs('password1', {'icon_left': 'fa-lock', 'is_horizontal': True})
        self.add_attrs('password2', {'icon_left': 'fa-lock', 'is_horizontal': True})
        self.add_attrs('access_token', {'icon_left': 'fa-key', 'is_horizontal': True})

    def clean_access_token(self):
        token = self.cleaned_data['access_token']
        try:
            AccessToken.objects.get(token=token)
        except AccessToken.DoesNotExist:
            raise ValidationError('Invalid access token')
        return token
