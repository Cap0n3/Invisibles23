# Generated by Django 4.1.7 on 2024-01-11 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0007_donationsection_alter_membershipsection_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="financialressources",
            options={
                "verbose_name": "Bibliothèque",
                "verbose_name_plural": "Bibliothèque",
            },
        ),
    ]
