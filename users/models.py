from django.contrib.auth.models import AbstractUser
from django.db import models

from config import NULLABLE


# Create your models here.


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    # avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', **NULLABLE)

    token = models.CharField(max_length=128, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.email}'
