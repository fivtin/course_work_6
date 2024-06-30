# Generated by Django 4.2.2 on 2024-06-30 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0015_newsletter_finish_alter_newsletter_frequency_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('set_block', 'Can enable / disable newsletter'), ('access_manager', 'Manager access to the newsletter')], 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='frequency',
            field=models.PositiveSmallIntegerField(choices=[(1, 'dayly'), (3, 'monthly'), (2, 'weekly')], default=1, verbose_name='периодичность'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(2, 'launched'), (3, 'completed'), (1, 'created')], default=1, verbose_name='статус'),
        ),
    ]