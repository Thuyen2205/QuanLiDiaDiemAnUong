# Generated by Django 5.0.1 on 2024-01-16 07:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealmaster', '0004_alter_thoidiem_thoi_gian_bat_dau_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='thoigianban',
            name='menu',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mealmaster.menu'),
            preserve_default=False,
        ),
    ]
