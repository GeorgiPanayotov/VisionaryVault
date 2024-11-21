import os

from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from VisionaryVaultApp.art.models import ArtPiece


@receiver(pre_delete, sender=ArtPiece)
def delete_art_piece_file(sender, instance, **kwargs):
    """Delete the file associated with the ArtPiece instance from the filesystem."""
    if instance.art_image:
        image_path = os.path.join(settings.MEDIA_ROOT, instance.art_image.name)
        if os.path.isfile(image_path):
            os.remove(image_path)

