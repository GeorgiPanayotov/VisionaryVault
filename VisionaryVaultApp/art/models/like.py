from django.db import models

from . import ArtPiece
from .user_related_model import UserRelatedModel
from .timestamp_status_model import TimestampStatusModel


class Like(UserRelatedModel, TimestampStatusModel):

    art_piece = models.ForeignKey(
        to=ArtPiece,
        on_delete=models.CASCADE,
        verbose_name='Art Piece'
    )

    class Meta:
        unique_together = ('user', 'art_piece')
