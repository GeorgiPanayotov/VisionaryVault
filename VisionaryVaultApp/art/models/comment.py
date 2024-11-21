from django.db import models
from .user_related_model import UserRelatedModel
from .timestamp_status_model import TimestampStatusModel
from .art_piece import ArtPiece


class Comment(UserRelatedModel, TimestampStatusModel):
    art_piece = models.ForeignKey(
        to=ArtPiece,
        on_delete=models.CASCADE
    )

    content = models.TextField()

    def __str__(self):
        return self.content

