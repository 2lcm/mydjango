# Generated by Django 4.2.11 on 2024-05-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_alter_review_table_comment'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='tag',
            name='blog_tag_name_43b6ed_idx',
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
