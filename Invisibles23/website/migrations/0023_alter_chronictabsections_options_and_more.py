# Generated by Django 4.1.7 on 2023-06-12 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0022_chronictabsections_delete_thematicsections"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="chronictabsections",
            options={
                "ordering": ["order"],
                "verbose_name": "Maladies chroniques",
                "verbose_name_plural": "Maladies chroniques",
            },
        ),
        migrations.AlterField(
            model_name="chronictabsections",
            name="order",
            field=models.PositiveIntegerField(
                blank=True,
                default=None,
                help_text="Laisser vide pour ajouter la section à la fin ou mettre 0 pour ne pas afficher la section",
                null=True,
                verbose_name="Ordre de la section",
            ),
        ),
    ]
