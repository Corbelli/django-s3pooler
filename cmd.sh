#!/bin/bash

set -e

if [[ $COMMAND = "worker" ]]; then
    echo "Running Celery Worker"
    exec celery worker -E -A s3eventscrapper --concurrency 1

elif [[ $COMMAND = "celerybeat" ]]; then
    echo "Running Celery Beat"
    exec celery beat -A s3eventscrapper --pidfile=/tmp/celerybeat.pid

elif [[ $COMMAND = "celeryflower" ]]; then
    echo "Running Celery Flower"
    exec celery flower -A s3eventscrapper

else
    echo "Running manage.py runserver"
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python manage.py shell
    exec python manage.py runserver 0:8000
fi
