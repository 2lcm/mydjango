# Generated by Django 4.2.11 on 2024-05-16 08:50

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_remove_tag_blog_tag_name_43b6ed_idx_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddIndex(
            model_name='tag',
            index=models.Index(fields=['name'], name='blog_tag_name_like', opclasses=['varchar_pattern_ops']),
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='blog_tag_name_unique'),
        ),
    ]