# Generated by Django 5.0.6 on 2024-05-15 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_reservation_amount_reservation_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_payment',
            field=models.BooleanField(default=False),
        ),
    ]
