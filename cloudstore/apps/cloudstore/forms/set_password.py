from django.contrib.auth.forms import SetPasswordForm
from django.forms import CharField, PasswordInput

from .bulma_mixin import BulmaMixin


class CloudstoreSetPasswordForm(BulmaMixin, SetPasswordForm):
    new_password1 = CharField(
        label='New password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'has-background-black-bis'}
        ),
    )
    new_password2 = CharField(
        label='Confirm new password',
        strip=False,
        widget=PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'has-background-black-bis'}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields()
        self.add_attrs(('new_password1', 'new_password2'), {'icon_left': 'fa-lock'})
