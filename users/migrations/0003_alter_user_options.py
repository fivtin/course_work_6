# Generated by Django 4.2.2 on 2024-06-30 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('view_list', 'Can view user list'), ('change_active', 'Can enable/disable active')], 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]