# Generated by Django 4.2.2 on 2024-06-29 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0007_alter_newsletter_frequency_alter_newsletter_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='frequency',
            field=models.PositiveSmallIntegerField(choices=[(3, 'monthly'), (1, 'dayly'), (2, 'weekly')], default=1, verbose_name='периодичность'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'created'), (2, 'launched'), (3, 'completed')], default=1, verbose_name='статус'),
        ),
    ]
