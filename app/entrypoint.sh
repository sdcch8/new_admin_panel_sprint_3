#!/bin/bash

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done

python manage.py collectstatic --noinput
python manage.py migrate movies 0001 --fake
python manage.py migrate

uwsgi --strict --ini uwsgi.ini
