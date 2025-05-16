# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt 

EXPOSE 5000

# Запускаем приложение
CMD ["python", "main.py"]