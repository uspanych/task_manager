from django.db import models
from django.db.models import Model


PRIORITY_CHOICES = (
    ('CRITICAL', 'critical'),
    ('HIGH', 'high'),
    ('MEDIUM', 'medium'),
    ('LOW', 'low')
)
TYPE_CHOICES = (
    ('BUG', 'bug'),
    ('TACK', 'tack')
)
STATUS_CHOICES = (
    ('to_do', 'To do'),
    ('In_progress', 'In progress'),
    ('Code_review', 'Code review'),
    ('Dev_test', "Dev test"),
    ('Testing', 'Testing'),
    ('Done', 'Done'),
    ('Wontfix', 'Wontfix')
)


RoleChoices = (
    ('manager', 'Менеджер'),
    ('teamlead', 'Тимлид'),
    ('developer', 'Разработчик'),
    ('test_engineer', 'Тест-инженер'),
)


class User(models.Model):
    login = models.CharField(verbose_name='Логин', unique=True, max_length=20)
    password = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=RoleChoices, null=True, blank=True)

    def __str__(self):
        return self.login


class Tacks(models.Model):
    title = models.CharField(
        max_length=20,
        verbose_name='Заголовок'
    )
    status = models.CharField(
        max_length=20, db_index=True,
        choices=STATUS_CHOICES,
        verbose_name='Статус'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Тип'
    )
    priority = models.CharField(
        max_length=20,
        db_index=True,
        choices=PRIORITY_CHOICES,
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
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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
