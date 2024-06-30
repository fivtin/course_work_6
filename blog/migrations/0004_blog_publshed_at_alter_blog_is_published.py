# Generated by Django 4.2.2 on 2024-06-30 19:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='publshed_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 30, 22, 52, 0, 557650), verbose_name='дата публикации'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='опубликовано'),
        ),
    ]