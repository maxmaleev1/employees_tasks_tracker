from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(
        User,  # Связываем с моделью пользователя
        on_delete=models.CASCADE,
        related_name='employee_profile'  # Для удобства обратной связи
    )
    full_name = models.CharField(max_length=255)  # ФИО сотрудника
    position = models.CharField(max_length=100)  # Должность сотрудника


    def __str__(self):
        return self.full_name


class Task(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начата'),      # задача ещё не началась
        ('in_progress', 'В работе'),       # задача в процессе
        ('completed', 'Выполнена'),        # задача завершена
    ]

    title = models.CharField(max_length=200)  # Наименование задачи
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks'
    )  # Исполнитель
    deadline = models.DateTimeField()  # Срок выполнения
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )  # Статус задачи
    parent_task = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subtasks')  # Родительская задача

    def __str__(self):
        return self.title
