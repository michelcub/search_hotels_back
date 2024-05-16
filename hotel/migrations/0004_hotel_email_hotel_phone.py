# Generated by Django 5.0.6 on 2024-05-16 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_services_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='hotel',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
