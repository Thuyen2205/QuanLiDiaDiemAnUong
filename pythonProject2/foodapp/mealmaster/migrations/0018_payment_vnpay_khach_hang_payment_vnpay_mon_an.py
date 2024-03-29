# Generated by Django 5.0.1 on 2024-02-23 08:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealmaster', '0017_alter_payment_vnpay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_vnpay',
            name='khach_hang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment_vnpay',
            name='mon_an',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mealmaster.monan'),
        ),
    ]
