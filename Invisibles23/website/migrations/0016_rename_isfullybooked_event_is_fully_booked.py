# Generated by Django 4.1.7 on 2024-07-16 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0015_remove_eventparticipants_isfullybooked_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="isFullyBooked",
            new_name="is_fully_booked",
        ),
    ]
