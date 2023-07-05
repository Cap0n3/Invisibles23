# Generated by Django 4.1.7 on 2023-07-05 08:43

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutsections",
            name="remote_image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, verbose_name="image"
            ),
        ),
        migrations.AddField(
            model_name="assosections",
            name="remote_image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, verbose_name="image"
            ),
        ),
        migrations.AddField(
            model_name="homesections",
            name="remote_image",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, verbose_name="image"
            ),
        ),
    ]
