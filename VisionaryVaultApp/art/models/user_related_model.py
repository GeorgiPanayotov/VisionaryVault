from django.conf import settings
from django.db import models


class UserRelatedModel(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True
