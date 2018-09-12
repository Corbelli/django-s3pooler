#!/bin/bash

set -e

if [[ $COMMAND = "s3poolerworker" ]]; then
    echo "Running Celery Worker"
    exec celery worker -E -A s3eventscrapper --concurrency 1 -Q celery

elif [[ $COMMAND = "visionsworker" ]]; then
    echo "Running Celery Worker"
    exec celery worker -E -A s3eventscrapper --concurrency 1  -Q users

elif [[ $COMMAND = "celerybeat" ]]; then
    echo "Running Celery Beat"
    exec celery beat -A s3eventscrapper --pidfile=/tmp/celerybeat.pid

elif [[ $COMMAND = "celeryflower" ]]; then
    echo "Running Celery Flower"
    exec celery flower -A s3eventscrapper

else
    echo "Running manage.py runserver"
    exec python manage.py runserver 0:8000
fi
