# Generated by Django 5.0.7 on 2024-08-21 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0017_alter_event_is_fully_booked_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="phone",
            field=models.CharField(
                blank=True, max_length=20, verbose_name="Numéro de téléphone"
            ),
        ),
    ]