from cloudinary.api import resources
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from cloudinary.models import CloudinaryField
from django.core.exceptions import ValidationError
from pathlib import Path
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator(object):
    def __init__(self, picture_size_mb: int, message=None):
        self.picture_size_mb = picture_size_mb
        self.message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, value):
        if value is None:
            self.__message = f"The picture size must be less than {self.picture_size_mb} MB."
        else:
            self.__message = value

    def __call__(self, value):
        # Ensure we are dealing with a Cloudinary resource
        if hasattr(value, 'public_id'):
            # Use Cloudinary's API to get image resource details
            image_metadata = resources(public_ids=[value.public_id])
            image_size = image_metadata['resources'][0]['bytes']  # Size in bytes

            # Check if the size exceeds the limit
            if image_size > self.picture_size_mb * 1024 * 1024:
                raise ValidationError(self.message)


"""Overridden FilesExtensionValidator for CloudinaryField"""


@deconstructible
class FileExtensionValidator:
    message = _(
        "File extension “%(extension)s” is not allowed. "
        "Allowed extensions are: %(allowed_extensions)s."
    )
    code = "invalid_extension"

    def __init__(self, allowed_extensions=None, message=None, code=None):
        if allowed_extensions is not None:
            allowed_extensions = [
                allowed_extension.lower() for allowed_extension in allowed_extensions
            ]
        self.allowed_extensions = allowed_extensions
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        # For CloudinaryField or CloudinaryResource
        if hasattr(value, 'url'):
            extension = Path(value.url).suffix[1:].lower()
        else:
            # For regular file fields
            raise ValidationError("File URL is not available in Cloudinary resource.")

        # Validate extension
        if self.allowed_extensions is not None and extension not in self.allowed_extensions:
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "extension": extension,
                    "allowed_extensions": ", ".join(self.allowed_extensions),
                    "value": value,
                },
            )
