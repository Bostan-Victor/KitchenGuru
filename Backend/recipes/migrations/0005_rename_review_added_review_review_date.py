# Generated by Django 4.2.5 on 2023-10-23 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_favorites'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='review_added',
            new_name='review_date',
        ),
    ]