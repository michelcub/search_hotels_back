# Generated by Django 5.0.6 on 2024-05-15 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='reservation',
        ),
    ]
