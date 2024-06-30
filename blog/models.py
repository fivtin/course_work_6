from django.db import models

from config import NULLABLE
from users.models import User


class Blog(models.Model):
    """ A class that implements the 'blog' model. """

    title = models.CharField(max_length=128, verbose_name='заголовок')
    slug = models.CharField(max_length=150)
    content = models.TextField( verbose_name='содержимое')
    preview = models.ImageField(upload_to='images/blog/', **NULLABLE,  verbose_name='превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='дата публикации')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='автор')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('id', )
