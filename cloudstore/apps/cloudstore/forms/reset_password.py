from django.contrib.auth.forms import PasswordResetForm
from django.forms import EmailField, EmailInput

from .bulma_mixin import BulmaMixin


class CloudstorePasswordResetForm(BulmaMixin, PasswordResetForm):
    email = EmailField(
        label='Email',
        max_length=254,
        widget=EmailInput(attrs={'autocomplete': 'email', 'class': 'has-background-black-bis'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_fields()
        self.add_attrs('email', {'icon_left': 'fa-envelope'})
