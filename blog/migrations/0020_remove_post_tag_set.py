# Generated by Django 4.2.11 on 2024-05-16 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_post_tag_set_posttagrelation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tag_set',
        ),
    ]
