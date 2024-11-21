from django.db import models
from VisionaryVaultApp.art.choices import CategoryType


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    category = models.TextField(
        choices=CategoryType.choices,
        default=CategoryType.OTHER,
        verbose_name='Art Category'
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.category_name
