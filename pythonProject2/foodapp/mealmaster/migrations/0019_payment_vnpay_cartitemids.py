# Generated by Django 5.0.1 on 2024-02-26 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mealmaster', '0018_payment_vnpay_khach_hang_payment_vnpay_mon_an'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment_vnpay',
            name='cartItemIds',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
