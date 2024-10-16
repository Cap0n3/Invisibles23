# Generated by Django 5.0.7 on 2024-10-17 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0033_volunteers_alter_aboutsections_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="volunteers",
            name="birthdate",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date de naissance"
            ),
        ),
        migrations.AlterField(
            model_name="volunteers",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Bénévole actif"),
        ),
    ]
