'''
Created on Apr 30, 2016

@author: takeelf
'''
from rest_framework.compat import unicode_to_repr
from rest_framework.exceptions import ValidationError
from rest_framework.utils.representation import smart_repr
from django.utils.translation import ugettext_lazy as _


class MinTogetherValidator(object):
    message = _('Ensure the fields {field_names} are greater than or equal to {amount}.')
    missing_message = _('This field is required.')

    def __init__(self, fields, min, message=None):
        self.fields = fields
        self.min = min
        self.message = message or self.message

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)

    def enforce_required_fields(self, attrs):
        if self.instance is not None:
            return

        missing = {
            field_name: self.missing_message
            for field_name in self.fields
            if field_name not in attrs
        }
        if missing:
            raise ValidationError(missing)

    def __call__(self, attrs):
        self.enforce_required_fields(attrs)
        checked_values = reduce(lambda x, y: x + y, [
            value for field, value in attrs.items() if field in self.fields
        ])
        if checked_values < self.min:
            field_names = ', '.join(self.fields)
            raise ValidationError(self.message.format(field_names=field_names, amount=self.min))

    def __repr__(self):
        return unicode_to_repr('<%s(fields=%s)>' % (
            self.__class__.__name__,
            smart_repr(self.fields)
        ))

