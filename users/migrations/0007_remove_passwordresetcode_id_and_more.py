# Generated by Django 4.2.4 on 2023-09-26 16:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_passwordresetcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='passwordresetcode',
            name='id',
        ),
        migrations.AlterField(
            model_name='passwordresetcode',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
