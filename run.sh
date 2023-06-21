#!/bin/bash

cd api/app

# Запуск миграций Django
python manage.py makemigrations
python manage.py migrate

python manage.py run

