from django.db import models


class CategoryType(models.TextChoices):
    PAINTING = 'PA', 'Painting'
    SCULPTURE = 'SC', 'Sculpture'
    DIGITAL_ART = 'DA', 'Digital Art'
    PHOTOGRAPHY = 'PH', 'Photography'
    INSTALLATION = 'IN', 'Installation'
    OTHER = 'OT', 'Other'

