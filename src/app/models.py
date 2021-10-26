from django.db import models
from django.db.models import Model


class User(models.Model):
    login = models.CharField(verbose_name='Логин', unique=True, max_length=256)
    password = models.CharField(max_length=256)
    role = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.login


class Task(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name='Заголовок'
    )
    status = models.CharField(
        max_length=20, db_index=True,
        verbose_name='Статус'
    )
    type = models.CharField(
        max_length=20,
        verbose_name='Тип'
    )
    priority = models.CharField(
        max_length=20,
        db_index=True,
        blank=True,
        verbose_name='Приоритет'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    executor = models.ForeignKey(
        User,
        verbose_name='Исполнитель',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='executor')
    creator = models.ForeignKey(
        User,
        verbose_name='Создатель',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='creator'
    )
    date_of_creation = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    date_of_change = models.DateField(
        auto_now=True,
        verbose_name='Дата изменения'
    )
