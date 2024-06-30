# Функция старта периодических задач
import smtplib
from datetime import datetime, timedelta
from calendar import monthrange

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config import settings
from mailer.models import Newsletter, Attempt


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()


def send_mailing():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Newsletter.objects.filter(
        status__in=[2, ],
        start__lte=current_datetime,
     )

    for mailing in mailings:
        last_attempt = Attempt.objects.filter(newsletter=mailing, success=True).order_by('-attempt_time').first()
        if last_attempt:
            last_attempt_time = last_attempt.attempt_time
        else:
            last_attempt_time = datetime.now(zone)  # = Attempt(newsletter=mailing, attempt_time=datetime.now(zone), )
        if mailing.frequency == 1:
            interval = timedelta(days=1)
        elif mailing.frequency == 2:
            interval = timedelta(days=7)
        elif mailing.frequency == 3:
            interval = timedelta(days=monthrange(last_attempt_time.year, last_attempt_time.month)[1])
        else:
            interval = timedelta(days=0)
        if not last_attempt or current_datetime >= last_attempt_time + interval:
            try:
                server_response = send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[client.email for client in mailing.clients.all()],
                    fail_silently=False,
                )
                Attempt.objects.create(newsletter=mailing, success=True, response=server_response)
            except smtplib.SMTPException as e:
                Attempt.objects.create(newsletter=mailing, response=e)
            except TimeoutError as e:
                Attempt.objects.create(newsletter=mailing, response=e)
