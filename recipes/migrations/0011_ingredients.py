# Generated by Django 4.2.4 on 2023-10-07 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_recipes_category_recipes_duration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('measurement_unit', models.CharField(choices=[('g', 'grams'), ('pcs', 'pieces'), ('ml', 'milliliters'), ('pcs', 'pieces'), ('tbsp', 'tablespoons'), ('tsp', 'teaspoons')], max_length=4)),
            ],
        ),
    ]
