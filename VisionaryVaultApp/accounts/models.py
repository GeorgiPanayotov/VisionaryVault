from datetime import date
from cloudinary.models import CloudinaryField
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from VisionaryVaultApp.accounts.managers import AppUserManager
from django.conf import settings
from django.db import models
from VisionaryVaultApp.accounts.validators import NameValidator


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True
    )

    username = models.CharField(
        unique=True
    )

    objects = AppUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    MAX_NAME_LENGTH = 20

    user = models.OneToOneField(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=[NameValidator()],
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=[NameValidator()],
        blank=False,
        null=False,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    profile_picture = CloudinaryField(
        null=True,
        blank=True,
        verbose_name='Profile Picture',
    )

    bio = models.TextField(
        blank=True
    )

    phone_number = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        validators=[RegexValidator(r'^\+?\d+$', 'Enter a valid phone number.')]
    )

    address = models.TextField(
        blank=True
    )

    class Meta:
        permissions = [
            ("can_moderate_comments", "Can moderate comments"),
            ("can_manage_artworks", "Can manage artworks"),
        ]

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        return None

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year
            if today.month < self.date_of_birth.month or \
                    (today.month == self.date_of_birth.month and today.day < self.date_of_birth.day):
                age -= 1
            return age
        return None

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize() if self.first_name else self.first_name
        self.last_name = self.last_name.capitalize() if self.last_name else self.last_name
        super().save(*args, **kwargs)
