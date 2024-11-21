# Generated by Django 5.1.2 on 2024-11-19 14:55

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0003_alter_artpiece_art_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='artpiece',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Price (USD)'),
            preserve_default=False,
        ),
    ]
