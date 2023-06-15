# Generated by Django 4.1.7 on 2023-06-06 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0008_rename_webpagesection_homepagesections"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutPageSections",
            fields=[
                (
                    "homepagesections_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="website.homepagesections",
                    ),
                ),
            ],
            bases=("website.homepagesections",),
        ),
    ]