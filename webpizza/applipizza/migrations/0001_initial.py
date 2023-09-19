# Generated by Django 4.2.5 on 2023-09-19 17:54

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                ("idIngredient", models.AutoField(primary_key=True, serialize=False)),
                (
                    "nomIngredient",
                    models.CharField(
                        max_length=50, verbose_name="le nom de cet ingrédient"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Pizza",
            fields=[
                ("idPizza", models.AutoField(primary_key=True, serialize=False)),
                (
                    "nomPizza",
                    models.CharField(
                        max_length=50, verbose_name="le nom de cette pizza"
                    ),
                ),
                (
                    "prix",
                    models.DecimalField(
                        decimal_places=2, max_digits=4, verbose_name="le prix"
                    ),
                ),
            ],
        ),
    ]
