# Generated by Django 4.2.4 on 2023-10-07 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredients',
            name='measurement_unit',
        ),
    ]