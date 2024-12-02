import os

from cloudinary import uploader
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from VisionaryVaultApp.art.models import ArtPiece

"""The function is triggered once a pre_delete signal is fired 
(before instance is deleted from the database) on Art piece model"""


@receiver(pre_delete, sender=ArtPiece)
def delete_art_piece_file(sender, instance, **kwargs):
    public_id = instance.art_image.public_id  # Get the public ID
    uploader.destroy(public_id)

