# Generated by Django 4.1.7 on 2023-06-14 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0028_baseressources_phone_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="baseressources",
            old_name="url",
            new_name="link",
        ),
    ]
