# Generated by Django 4.2.5 on 2023-11-02 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_rename_image_url_airecipes_image_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airecipes',
            name='image_field',
            field=models.ImageField(default='static/recipes/no_recipe.jpg', upload_to='ai_recipes/'),
        ),
    ]