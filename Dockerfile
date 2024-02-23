FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# run needed migrations to create database scheme
RUN python manage.py makemigrations
RUN python manage.py migrate
# change superuser password in .env - $DJANGO_SUPERUSER_PASSWORD
RUN python manage.py createsuperuser --noinput \
    --username admin \
    --email admin@example.com

# run fixtures to fill database with mock data
RUN python manage.py loaddata categories.json
RUN python manage.py loaddata tasks.json

CMD ["sh", "-c", "cp .env.example .env && python manage.py runserver 0.0.0.0:8000"]
