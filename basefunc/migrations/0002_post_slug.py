# Generated by Django 4.2.1 on 2024-02-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basefunc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255),
        ),
    ]
