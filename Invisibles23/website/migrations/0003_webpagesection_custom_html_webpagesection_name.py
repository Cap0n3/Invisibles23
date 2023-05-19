# Generated by Django 4.1.7 on 2023-05-12 15:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_alter_webpagesection_text"),
    ]

    operations = [
        migrations.AddField(
            model_name="webpagesection",
            name="custom_html",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="webpagesection",
            name="name",
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]