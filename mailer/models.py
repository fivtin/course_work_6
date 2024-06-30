from django.db import models

from config import NULLABLE
from users.models import User


# Create your models here.


class Client(models.Model):

    email = models.EmailField(max_length=256, unique=True, verbose_name='e-mail')
    fio = models.CharField(max_length=128, verbose_name='ф.и.о.')
    info = models.TextField(verbose_name='комментарий')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
        # ordering = ('id',)

    def __str__(self):
        return f'{self.email} ({self.fio})'


class Message(models.Model):

    subject = models.CharField(max_length=256, verbose_name='тема')
    body = models.TextField(verbose_name='содержимое')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщений'

    def __str__(self):
        return self.subject


class Newsletter(models.Model):
    FREQUENCY_CHOICES = {
        (1, "dayly"),
        (2, "weekly"),
        (3, "monthly"),
    }
    STATUS_CHOICES = {
        (1, "created"),
        (2, "launched"),
        (3, "completed"),
    }
    title = models.CharField(max_length=128, verbose_name='название')
    start = models.DateTimeField(verbose_name='время начала')
    finish = models.DateTimeField(verbose_name='время окончания', **NULLABLE)
    frequency = models.PositiveSmallIntegerField(choices=FREQUENCY_CHOICES, default=1, verbose_name='периодичность')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='сообщение')
    clients = models.ManyToManyField(Client, verbose_name='получатели')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='владелец')
    is_block = models.BooleanField(default=False, verbose_name="заблокировано")

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

        permissions = [
            ('set_block', 'Can enable / disable newsletter'),
            ('access_manager', 'Manager access to the newsletter'),
        ]

    def __str__(self):
        return f'{self.title}({self.status}): {self.start}-{self.frequency}'


class Recipient(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'

    def __str__(self):
        return f'{self.newsletter.title}: {self.client.email}'


class Attempt(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE, **NULLABLE, verbose_name='рассылка')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='время попытки')
    success = models.BooleanField(default=False, verbose_name='успешно')
    response = models.TextField(verbose_name='ответ сервера')


