from django.db import models


class TimestampStatusModel(models.Model):
    status = models.CharField(
        max_length=20,
        default='active'  # e.g., active, reported
    )
    timestamp = models.DateTimeField(
        auto_now_add=True  # Automatically set to now when created
    )

    class Meta:
        abstract = True
