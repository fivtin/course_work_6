import smtplib
from datetime import datetime, timedelta
from calendar import monthrange

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail

from config import settings
from mailer.models import Newsletter, Attempt


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=60)
    scheduler.start()


def send_mailing():
    current_datetime = datetime.now()
    mailings = Newsletter.objects.filter(
        status__in=[1, 2, ],
        start__lte=current_datetime,
        is_block=False,
    )
    for mailing in mailings:
        if mailing.is_block:
            continue
        if mailing.finish and current_datetime > mailing.finish:
            mailing.status = 3
            mailing.save()
            continue
        if mailing.status == 1 and current_datetime > mailing.start:
            mailing.status = 2
            mailing.save()
        last_attempt = Attempt.objects.filter(newsletter=mailing, success=True).order_by('-attempt_time').first()
        if last_attempt:
            last_attempt_time = last_attempt.attempt_time
        else:
            last_attempt_time = datetime.now()
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
                clients = [client.email for client in mailing.clients.all()]
                from_email = settings.EMAIL_HOST_USER
                server_response = send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    from_email,
                    clients,
                    fail_silently=False,
                )
                Attempt.objects.create(newsletter=mailing, success=True, response=server_response)
            except smtplib.SMTPException as e:
                Attempt.objects.create(newsletter=mailing, response=e)
