from django.db import models

from VisionaryVaultApp.art.models import ArtPiece
from VisionaryVaultApp.art.models import UserRelatedModel


class Basket(UserRelatedModel):
    pass


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    art_piece = models.ForeignKey(ArtPiece, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('basket', 'art_piece')

    @property
    def total_price(self):
        return self.quantity * self.art_piece.price
