# Generated by Django 5.0.7 on 2024-10-18 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0035_alter_volunteers_role"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="volunteers",
            options={
                "verbose_name": "BDD - Bénévole",
                "verbose_name_plural": "BDD - Bénévoles",
            },
        ),
    ]
