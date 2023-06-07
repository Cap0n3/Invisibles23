# Generated by Django 4.1.7 on 2023-06-07 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0009_aboutpagesections"),
    ]

    operations = [
        migrations.CreateModel(
            name="YoutubeVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                ("short_url", models.CharField(max_length=50)),
            ],
        ),
    ]
