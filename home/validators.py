from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def max_length_validator(maxlength, field):
    def inner_validate_fn(value):
        if len(value) > maxlength:
            raise ValidationError(_('%s is too long!!' % field))
    return inner_validate_fn
