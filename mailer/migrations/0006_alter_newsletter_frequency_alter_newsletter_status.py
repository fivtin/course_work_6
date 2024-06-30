# Generated by Django 4.2.2 on 2024-06-29 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailer', '0005_alter_newsletter_clients_alter_newsletter_frequency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='frequency',
            field=models.PositiveSmallIntegerField(choices=[(2, 'weekly'), (3, 'monthly'), (1, 'dayly')], default=1, verbose_name='периодичность'),
        ),
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(2, 'launched'), (3, 'completed'), (1, 'created')], default=1, verbose_name='статус'),
        ),
    ]
