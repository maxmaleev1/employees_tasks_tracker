from django.contrib.auth.models import User
from employees_tasks.models import Employee, Task
from django.utils import timezone
from datetime import timedelta
import random

User.objects.all().delete()
Employee.objects.all().delete()
Task.objects.all().delete()

admin_user = User.objects.create_superuser(
    username='руководов_рр',
    password='123456'
)

Employee.objects.create(
    user=admin_user,
    full_name='Руководитель Руководительевич Руководов',
    position='Руководитель отдела разработки'
)

names = [
    ('Алексей', 'Петрович', 'Иванов'),
    ('Мария', 'Сергеевна', 'Кузнецова'),
    ('Игорь', 'Андреевич', 'Сидоров'),
    ('Елена', 'Викторовна', 'Морозова'),
    ('Дмитрий', 'Иванович', 'Васильев'),
    ('Ольга', 'Николаевна', 'Павлова'),
    ('Сергей', 'Алексеевич', 'Михайлов'),
    ('Анна', 'Дмитриевна', 'Новикова'),
    ('Владимир', 'Петрович', 'Фёдоров'),
    ('Татьяна', 'Сергеевна', 'Беляева')
]

positions = [
    'Разработчик Python',
    'Разработчик Frontend',
    'Тестировщик',
    'Бизнес-аналитик',
    'DevOps-инженер',
    'Системный архитектор',
    'Менеджер проектов',
    'UX/UI дизайнер',
    'Скрам-мастер',
    'Системный администратор'
]

employees = []
for i, (name, patronymic, surname) in enumerate(names):
    username = f'{surname.lower()}_{name[0].lower()}{patronymic[0].lower()}'
    user = User.objects.create_user(
        username=username,
        password='123456'
    )
    employee = Employee.objects.create(
        user=user,
        full_name=f'{name} {patronymic} {surname}',
        position=positions[i]
    )
    employees.append(employee)

task_titles = [
    'Разработка REST API',
    'Верстка интерфейса',
    'Покрытие тестами',
    'Настройка CI/CD',
    'Проработка требований',
    'Проектирование базы данных',
    'Создание прототипов',
    'Рефакторинг кода',
    'Написание документации',
    'Настройка мониторинга',
    'Внедрение логирования',
    'Анализ рисков',
    'Обновление зависимостей',
    'Оптимизация производительности',
    'Подготовка релиза'
]

all_tasks = []

for i in range(30):
    title = random.choice(task_titles)
    employee = random.choice(employees)

    if i < 2:
        deadline = timezone.now() - timedelta(days=random.randint(1,5))
    else:
        deadline = timezone.now() + timedelta(days=random.randint(2,15))

    status = random.choice(['not_started', 'in_progress', 'completed'])

    task = Task.objects.create(
        title=title,
        deadline=deadline,
        status=status,
        employee=employee
    )
    all_tasks.append(task)

for i in range(5):
    child_task = random.choice(all_tasks)
    parent_task = random.choice(all_tasks)
    if child_task != parent_task:
        child_task.parent_task = parent_task
        child_task.save()

print('Создание данных завершено.')
