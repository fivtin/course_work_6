from django.apps import AppConfig


class MailerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailer'

    """
    def ready(self):
         from имя_приложения.модуль_с_задачей import функция_старта 
         sleep(2)
         функция_старта()
    """