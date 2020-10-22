from django.core.exceptions import ValidationError
from django.db.models import Model
from django.forms import CharField, Form, PasswordInput

from .bulma_mixin import BulmaMixin


class ResourcePasswordForm(BulmaMixin, Form):
    password = CharField(
        label='Password',
        strip=False,
        widget=PasswordInput(attrs={'autocomplete': 'off', 'class': 'has-background-black-bis'}),
    )

    resource: Model

    def __init__(self, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resource = resource
        self.update_fields()
        self.add_attrs('password', {'icon_left': 'fa-lock'})

    def clean_password(self):
        data = self.cleaned_data['password']
        if self.resource.share.matches(data):
            return data
        raise ValidationError('Invalid password')
