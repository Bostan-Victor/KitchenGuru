# Generated by Django 4.2.4 on 2023-09-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profiles_id_alter_profiles_last_login_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='first_name',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='last_name',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
