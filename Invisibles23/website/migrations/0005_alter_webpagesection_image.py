# Generated by Django 4.1.7 on 2023-05-12 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_alter_webpagesection_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="webpagesection",
            name="image",
            field=models.ImageField(upload_to=""),
        ),
    ]
