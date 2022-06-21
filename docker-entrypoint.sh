#!/bin/bash

# Wait for Postgres to become available
while ! nc -z api_database 5432; do 
  sleep 1
done

python manage.py makemigrations
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000