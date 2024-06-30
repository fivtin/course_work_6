from django.contrib.auth.models import AbstractUser
from django.db import models

from config import NULLABLE


# Create your models here.


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='email')

    first_name = models.CharField(max_length=150, verbose_name="Имя")
    last_name = models.CharField(max_length=150, default="", **NULLABLE, verbose_name="Фамилия")

    phone = models.CharField(max_length=20, **NULLABLE, verbose_name='телефон')
    image = models.ImageField(upload_to='users/avatars/', **NULLABLE, verbose_name="аватар")

    token = models.CharField(max_length=128, verbose_name='токен', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

        permissions = [
            ('view_list', 'Can view user list'),
            ('change_active', 'Can enable/disable active'),
        ]

    def __str__(self):
        return f'{self.email}'
