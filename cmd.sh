#!/bin/bash

set -e

if [[ $COMMAND = "celeryworker" ]]; then
    echo "Running Celery Worker"
    exec celery worker -E -A s3eventscrapper

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
