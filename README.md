# Трекер задач сотрудников

Проект представляет собой систему для управления задачами внутри компании.
Руководители (админы) могут создавать и удалять задачи и сотрудников.
Сотрудники могут менять статус назначенных им задач.  
Все пользователи могут просматривать задачи и сотрудников.

---

## 🚧 Стек технологий

- Python 3.12  
- Django 5.2.3  
- Django REST Framework  
- PostgreSQL  
- Docker, Docker Compose  
- Redis, Celery (для фоновых задач)  
- JWT (аутентификация)  
- pytest (тестирование)

---

## 📁 Структура проекта

```
employees_tasks_tracker/     # Корень проекта
│
├── config/                  # Настройки Django
├── employees/               # Приложение для сотрудников
├── tasks/                   # Приложение для задач
│
├── manage.py
├── docker-compose.yml
├── Dockerfile
├── .env.example
├── README.md
```

---

## ⚙️ Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/maxmaleev1/employees_tasks_tracker.git
cd employees_tasks_tracker
```

### 2. Настроить переменные окружения

Создайте `.env` файл на основе `.env.example`:

```bash
cp .env.example .env
```

Убедитесь, что указаны параметры подключения к PostgreSQL.

### 3. Собрать и запустить контейнеры

```bash
docker-compose up --build
```

### 4. Применить миграции и создать суперпользователя

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. (Опционально) Собрать статику

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

---

## 🧪 Тесты

```bash
docker-compose exec web pytest --cov
```

Покрытие тестами: **100%**

---

## 🔑 Аутентификация

Для доступа к защищённым маршрутам используется JWT.  
Получение токенов:

```http
POST /employees_tasks/api/token/
{
  "username": "your_username",
  "password": "your_password"
}
```

Ответ:

```json
{
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

---

## 📌 Основные эндпоинты API

| Метод | URL                                   | Описание                          |
|-------|----------------------------------------|-----------------------------------|
| GET   | /employees_tasks/employees/           | Список сотрудников                |
| POST  | /employees_tasks/employees/           | Добавить сотрудника (только админ)|
| DELETE| /employees_tasks/employees/{id}/      | Удалить сотрудника (только админ) |
| GET   | /employees_tasks/tasks/               | Список задач                      |
| POST  | /employees_tasks/tasks/               | Создать задачу (только админ)     |
| PATCH | /employees_tasks/tasks/{id}/          | Обновить статус (исполнитель)     |
| DELETE| /employees_tasks/tasks/{id}/          | Удалить задачу (только админ)     |
| GET   | /employees_tasks/tasks/overdue/       | Просроченные задачи               |
| GET   | /employees_tasks/tasks/important/     | Важные задачи                     |
| GET   | /employees_tasks/tasks/busy_employees/| Сотрудники с наибольшей загрузкой |

---

## 📚 Автодокументация

После запуска проекта доступна по адресу:

```
http://localhost:8000/employees_tasks/docs/
```

---

## 🔗 Репозиторий

https://github.com/maxmaleev1/employees_tasks_tracker
