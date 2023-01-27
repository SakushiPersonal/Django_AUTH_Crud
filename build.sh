#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install

pip install -r requirements.txt


python manage.py collectstatic --noinput
python manage.py migrate


python manage.py createsuperuser --username --noinput
python manage.py createsuperuser --password --noinput
python manage.py createsuperuser --email --noinput