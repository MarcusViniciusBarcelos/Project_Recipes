# Generated by Django 4.2.5 on 2023-10-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0004_alter_recipe_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="title",
            field=models.CharField(max_length=65, verbose_name="Title"),
        ),
    ]
