# Generated by Django 4.2.5 on 2023-09-16 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_options_alter_users_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
