# Generated by Django 4.2.1 on 2024-03-20 19:07

import autoslug.fields
import basefunc.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basefunc', '0013_alter_category_options_alter_category_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='autoslug',
            field=autoslug.fields.AutoSlugField(default='test', editable=False, populate_from='title', slugify=basefunc.models.custom_slugify),
            preserve_default=False,
        ),
    ]