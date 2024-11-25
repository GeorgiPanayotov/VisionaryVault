from decimal import Decimal

from cloudinary.models import CloudinaryField
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from .user_related_model import UserRelatedModel
from .timestamp_status_model import TimestampStatusModel
from VisionaryVaultApp.art.validators import FileSizeValidator


class ArtPiece(UserRelatedModel, TimestampStatusModel):

    art_image = CloudinaryField(
        verbose_name='Art Picture',
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg']),
            FileSizeValidator(6)
        ],
        null=False,
        blank=False
    )

    description = models.TextField(
        max_length=200,
        null=True,
        blank=True
    )

    categories = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='art_pieces',
        null=False,
        blank=False
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Price (USD)"
    )

    def likes_count(self):
        return self.like_set.count()

    def __str__(self):
        return self.description
