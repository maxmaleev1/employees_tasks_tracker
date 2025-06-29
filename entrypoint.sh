#!/bin/sh

# Прерываем выполнение при любой ошибке
set -e

# Выполняем миграции перед запуском сервера
echo "🛠️ Применяем миграции..."
python manage.py migrate

# Собираем статические файлы (для продакшна, но безопасно и в dev)
echo "📦 Собираем статические файлы..."
python manage.py collectstatic --noinput

## Запускаем Gunicorn (WSGI сервер)
#echo "🚀 Запускаем Gunicorn..."
#gunicorn config.wsgi:application \
#  --bind 0.0.0.0:8000 \
#  --timeout 120

# Запускаем Django runserver для разработки
exec python manage.py runserver 0.0.0.0:8000