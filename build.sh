#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install

pip install -r requirements.txt


python manage.py collectstatic --noinput
python manage.py migrate

#if User.objects.filter(username=sakushi).count():
  #python manage.py createsuperuser --noinput
  #python manage.py createsuperuser --password --noinput
  #python manage.py createsuperuser --email --noinput