from django.conf import settings
from django.db import models
from VisionaryVaultApp.art.models import ArtPiece, Comment  # Import other relevant models


class Report(models.Model):

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    art_piece = models.ForeignKey(
        to=ArtPiece,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        to=Comment,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

