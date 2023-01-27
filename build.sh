#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install

pip install -r requirements.txt


python manage.py collectstatic --no-input
python manage.py migrate


echo "from django.contrib.auth import get_user_model;
 User = get_user_model();
  User.objects.create_superuser('sakushi', 'sakushi@myproject.com', '_M@ranatha97')" | python manage.py shell