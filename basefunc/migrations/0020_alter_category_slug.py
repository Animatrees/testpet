# Generated by Django 4.2.1 on 2024-03-20 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basefunc', '0019_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]