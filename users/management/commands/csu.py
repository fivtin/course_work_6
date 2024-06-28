import os

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create(email=os.getenv('SUPERUSER_LOGIN'))
        user.set_password(os.getenv('SUPERUSER_PASSWORD'))
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
