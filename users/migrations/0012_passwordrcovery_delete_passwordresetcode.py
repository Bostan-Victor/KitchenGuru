# Generated by Django 4.2.4 on 2023-09-30 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_passwordresetcode_is_used'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordRcovery',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(null=True)),
                ('is_used', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='PasswordResetCode',
        ),
    ]
