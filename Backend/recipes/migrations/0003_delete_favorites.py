# Generated by Django 4.2.5 on 2023-10-09 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_favorites_a'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorites',
        ),
    ]
