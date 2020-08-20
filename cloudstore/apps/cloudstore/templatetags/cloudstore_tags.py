from hashlib import md5
from urllib.parse import urlencode as enc

from django import forms, template
from django.conf import settings

register = template.Library()

gr_url = 'https://www.gravatar.com/avatar/'


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def is_file(field):
    return isinstance(field.field.widget, forms.FileInput)


@register.filter
def gravatar(user, size: int = 32):
    email_hash = md5(user.email.lower().encode('utf-8')).hexdigest()  # nosec
    return f'{gr_url}{email_hash}?{enc({"s":size,"d":"retro"})}'


@register.filter
def debug_dir(obj):
    if settings.DEBUG:
        return dir(obj)
    return obj
