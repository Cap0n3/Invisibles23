# Generated by Django 5.0.7 on 2024-10-15 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0026_alter_adminressources_options_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="membershipplans",
            unique_together={("name", "price", "frequency")},
        ),
    ]
