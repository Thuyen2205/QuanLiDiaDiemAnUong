# Generated by Django 5.0.1 on 2024-01-23 08:58

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mealmaster', '0010_alter_monan_hinh_anh'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='hinh_anh',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='avatar'),
        ),
    ]
