# Generated by Django 5.0.1 on 2024-01-26 20:16

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mealmaster', '0013_taikhoan_dia_chi'),
    ]

    operations = [
        migrations.AddField(
            model_name='loaithucan',
            name='hinh_anh',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True, verbose_name='hinh_anh'),
        ),
    ]