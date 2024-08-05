# Generated by Django 4.2.1 on 2024-03-20 19:30

import autoslug.fields
import basefunc.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basefunc', '0015_remove_category_autoslug_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='title', slugify=basefunc.models.custom_slugify, unique=True),
        ),
    ]