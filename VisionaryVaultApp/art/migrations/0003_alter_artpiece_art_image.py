# Generated by Django 5.1.2 on 2024-11-10 17:14

import VisionaryVaultApp.art.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0002_alter_artpiece_art_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artpiece',
            name='art_image',
            field=models.ImageField(upload_to='', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), VisionaryVaultApp.art.validators.FileSizeValidator(6)], verbose_name='Art Picture'),
        ),
    ]
