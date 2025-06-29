# Используем официальный Python-образ
FROM python:3.11

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем curl (нужен для установки poetry)
RUN apt-get update && apt-get install -y curl

# Копируем только pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем poetry
RUN curl -sSL https://install.python-poetry.org | python3 && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Отключаем создание виртуального окружения и устанавливаем зависимости (без установки проекта)
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --with dev

# Копируем остальной код проекта
COPY . /app

# Делаем entrypoint.sh исполняемым
RUN chmod +x entrypoint.sh

# Указываем скрипт entrypoint
ENTRYPOINT ["./entrypoint.sh"]
