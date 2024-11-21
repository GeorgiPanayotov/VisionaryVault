# Generated by Django 5.1.2 on 2024-11-10 16:41

import VisionaryVaultApp.art.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artpiece',
            name='art_image',
            field=models.ImageField(upload_to='static/images/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg']), VisionaryVaultApp.art.validators.FileSizeValidator(6)], verbose_name='Art Picture'),
        ),
    ]
