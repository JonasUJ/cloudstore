from typing import Dict, Sequence, Union

from django.forms import CheckboxInput, Field


class BulmaMixin:
    '''
    Mixin for handling Bulma classes in a Form
    '''

    def update_fields(self):
        for name, field in self.fields.items():
            if self.has_error(name):
                self.add_classes(field, 'is-danger')
            if not isinstance(field.widget, CheckboxInput):
                self.add_classes(field, 'input')
            else:
                self.add_classes(field, 'is-checkradio')

    @staticmethod
    def add_classes(field: Field, class_string: str) -> None:
        if not field.widget.attrs.get('class', False):
            field.widget.attrs['class'] = ''
        field.widget.attrs['class'] += ' ' + class_string

    def add_attrs(self, field_names: Union[str, Sequence[str]], attrs: Dict[str, str]):
        if isinstance(field_names, str):
            field_names = {field_names}
        for field in field_names:
            for name, val in attrs.items():
                setattr(self.fields[field], name, val)
