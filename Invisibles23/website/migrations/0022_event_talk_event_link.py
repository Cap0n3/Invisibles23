# Generated by Django 5.0.7 on 2024-09-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0021_participant_country"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="talk_event_link",
            field=models.URLField(blank=True),
        ),
    ]
