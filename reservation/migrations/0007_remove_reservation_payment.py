# Generated by Django 5.0.6 on 2024-05-15 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_reservation_is_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='payment',
        ),
    ]
