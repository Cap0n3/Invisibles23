# Generated by Django 4.1.7 on 2023-06-10 12:49

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0018_rename_bodytext_thematicsections_content_html_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="thematicsections",
            name="content_html",
            field=ckeditor.fields.RichTextField(verbose_name="Contenu de la section"),
        ),
        migrations.AlterField(
            model_name="thematicsections",
            name="tab",
            field=models.CharField(
                choices=[
                    ("chronic", "Maladies chroniques"),
                    ("invisible", "Maladies invisibles"),
                    ("miscarriage", "Fausses couches"),
                ],
                default="chronique",
                max_length=20,
                verbose_name="Onglet associé",
            ),
        ),
    ]