import re
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class NameValidator:
    def __init__(self, message=None):
        self.message = message or 'Ensure you first and last name are containing only letters.'

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None or value == "":
            self.__message = "Please enter both your first and last name"
        else:
            self.__message = value

    def __call__(self, value):
        pattern = re.compile(r"^[A-Za-z]+$")
        if not re.match(pattern, value):
            raise ValidationError(self.message)


def validate_custom_password(password):
    """ Custom password validation requirements. """
    if len(password) < 8:
        raise ValidationError(_("Password must be at least 8 characters long."))
    if not any(char.isdigit() for char in password):
        raise ValidationError(_("Password must contain at least one digit."))
    if not any(char.isupper() for char in password):
        raise ValidationError(_("Password must contain at least one uppercase letter."))

