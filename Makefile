#!/bin/bash
.PHONY: default
.SILENT:

default:

_local_env:
	-cp -n local.env.sample local.env

shell: _local_env
	docker-compose exec  django bash

migrate: _local_env
	docker-compose run --rm django python manage.py migrate --noinput

mkmigrations: _local_env
	docker-compose exec django python manage.py makemigrations

start: migrate
	docker-compose up -d

stopw:
	docker-compose stop celeryworker

startw:
	docker-compose start celeryworker

worker:
	clear
	docker-compose logs -f --tail=1  celeryworker

stop: _local_env
	docker-compose down -v

registered: _local_env
	docker-compose  exec celeryworker celery inspect registered

restart-celery:
	docker-compose restart celeryworker celerybeat

build:
	docker-compose build --force-rm --no-cache --pull

logs:
	docker-compose logs --follow

clean-containers:
	-docker ps -aqf ancestor=eventlogger_* | xargs docker rm -f

clean-images:
	-docker images -q -f reference=eventlogger_* | xargs docker rmi -f

clean-volumes:
	-docker volume ls -q -f name=eventlogger_* | xargs docker volume rm -f

clean-layers:
	-docker images -q -f dangling=true | xargs docker rmi -f

clean-all: stop clean-containers clean-images clean-volumes clean-layers
