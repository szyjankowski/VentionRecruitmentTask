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

# create superuser
ENV DJANGO_SUPERUSER_PASSWORD admin
RUN python manage.py createsuperuser --noinput --username admin --email admin@example.com



# run fixtures to fill database with mock data
RUN python manage.py loaddata fixtures/categories.json
RUN python manage.py loaddata fixtures/tasks.json

CMD ["sh", "-c", "cp .env.example .env && python manage.py runserver 0.0.0.0:8000"]
