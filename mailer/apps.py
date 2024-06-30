from time import sleep

from django.apps import AppConfig


class MailerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailer'

    def ready(self):
        from services.scheduler import start
        sleep(2)
        start()
