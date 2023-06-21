# Generated by Django 4.1.7 on 2023-06-21 12:35

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0036_homepagesections_reverse"),
    ]

    operations = [
        migrations.CreateModel(
            name="HomeSections",
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
                ("name", models.CharField(max_length=50)),
                ("title", models.CharField(max_length=50)),
                (
                    "richText",
                    ckeditor.fields.RichTextField(
                        default="Écrire ici",
                        max_length=10000,
                        verbose_name="Contenu de la section",
                    ),
                ),
                ("text", models.TextField(max_length=10000)),
                ("custom_html", models.TextField(blank=True)),
                ("image", models.ImageField(upload_to="")),
                ("image_title", models.CharField(blank=True, max_length=50)),
                ("image_alt", models.CharField(blank=True, max_length=50)),
                (
                    "reverse",
                    models.BooleanField(
                        default=False,
                        verbose_name="Inverser l'ordre de l'image et du texte",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page d'accueil",
                "verbose_name_plural": "Page d'accueil",
            },
        ),
    ]
