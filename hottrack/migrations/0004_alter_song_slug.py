# Generated by Django 4.2.11 on 2024-05-15 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hottrack', '0003_populate_song_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='slug',
            field=models.SlugField(allow_unicode=True, blank=True, max_length=100),
        ),
    ]
