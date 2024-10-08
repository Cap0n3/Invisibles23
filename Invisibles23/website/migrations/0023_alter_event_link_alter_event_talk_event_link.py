# Generated by Django 5.0.7 on 2024-09-27 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0022_event_talk_event_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="link",
            field=models.URLField(
                blank=True, verbose_name="Lien de l'événement (optionnel)"
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="talk_event_link",
            field=models.URLField(blank=True, verbose_name="Lien de réunion Zoom"),
        ),
    ]
