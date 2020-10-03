from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import BooleanField, CharField, PasswordInput, TextInput

from .bulma_mixin import BulmaMixin


class LoginForm(BulmaMixin, AuthenticationForm):
    username = UsernameField(
        label='Username',
        widget=TextInput(
            attrs={
                'autofocus': True,
                'autocomplete': 'username',
                'class': 'has-background-black-bis',
            }
        ),
    )
    password = CharField(
        label='Password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'has-background-black-bis'}
        ),
        # NOTE: Can't use reverse() for "/account/password_reset" here
        help_text='<a href="/account/password_reset">I forgot my password</a>',
    )
    remember_me = BooleanField(
        label='',
        required=False,
        help_text='Remember me',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields()
        self.add_attrs('username', {'icon_left': 'fa-user'})
        self.add_attrs('password', {'icon_left': 'fa-lock'})
