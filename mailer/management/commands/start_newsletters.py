import os

from django.core.management import BaseCommand

from services.scheduler import send_mailing


class Command(BaseCommand):

    def handle(self, *args, **options):

        send_mailing()
