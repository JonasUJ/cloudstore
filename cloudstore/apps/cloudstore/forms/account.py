from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UsernameField
from django.forms import CharField, EmailField, ModelForm, PasswordInput, TextInput

from .bulma_mixin import BulmaMixin


class UserEditForm(BulmaMixin, ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email']

    username = UsernameField(
        label='Username',
        max_length=25,
        widget=TextInput(
            attrs={'autocomplete': 'username',
                   'class': 'has-background-black-bis'}),
    )
    email = EmailField(
        label='E-mail address',
        widget=TextInput(
            attrs={'autocomplete': 'email',
                   'class': 'has-background-black-bis'}),
        help_text='Used for password resets'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields()
        self.add_attrs('username', {'icon_left': 'fa-user', 'is_horizontal': True})
        self.add_attrs('email', {'icon_left': 'fa-envelope', 'is_horizontal': True})


class CloudstorePasswordChangeForm(BulmaMixin, PasswordChangeForm):
    old_password = CharField(
        label='Old password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'password',
                   'class': 'has-background-black-bis'}),
    )
    new_password1 = CharField(
        label='New password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'class': 'has-background-black-bis'}),
    )
    new_password2 = CharField(
        label='Confirm new password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'new-password',
                   'class': 'has-background-black-bis'}),
        help_text='Enter the same password as before, for verification.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields()
        self.add_attrs(('old_password',
                        'new_password1',
                        'new_password2'),
                       {'icon_left': 'fa-lock', 'is_horizontal': True})