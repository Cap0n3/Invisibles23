# Generated by Django 4.1.7 on 2024-07-15 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0009_eventparticipants_participant_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="is_talk_event",
            field=models.BooleanField(
                default=False, verbose_name="Évènement de type groupe de parole"
            ),
        ),
    ]