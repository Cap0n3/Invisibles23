# Generated by Django 4.1.7 on 2023-06-27 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0043_assostatus"),
    ]

    operations = [
        migrations.RenameField(
            model_name="assostatus",
            old_name="text",
            new_name="richText",
        ),
    ]