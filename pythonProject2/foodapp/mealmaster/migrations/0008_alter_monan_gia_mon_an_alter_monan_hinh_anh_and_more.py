# Generated by Django 5.0.1 on 2024-01-16 08:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealmaster', '0007_alter_thoigianban_mon_an'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monan',
            name='gia_mon_an',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='monan',
            name='hinh_anh',
            field=models.ImageField(blank=True, null=True, upload_to='monan/%y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='monan',
            name='loai_thuc_an',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mealmaster.loaithucan'),
        ),
        migrations.AlterField(
            model_name='monan',
            name='mo_ta',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='monan',
            name='nguoi_dung',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='monan',
            name='so_luong',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='monan',
            name='ten_mon_an',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='monan',
            name='trang_thai',
            field=models.BooleanField(default=True),
        ),
    ]
