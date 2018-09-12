#!/bin/bash
.PHONY: default
.SILENT:

default:

_local_env:
	-cp -n local.env.sample local.env

shell: _local_env
	docker-compose exec  django bash

mkmigrations: _local_env
	docker-compose exec django python manage.py makemigrations

migrate: mkmigrations
	docker-compose run --rm django python manage.py migrate --noinput

start:
	docker-compose up -d

stopws:
	docker-compose stop visionsworker s3poolerworker

startws:
	docker-compose start visionsworker s3poolerworker

raw-w:
	clear
	docker-compose logs -f --tail=1  s3poolerworker

visions-w:
	clear
	docker-compose logs -f --tail=1  visionsworker

stop: _local_env
	docker-compose down -v

registered: _local_env
	docker-compose  exec s3poolerworker celery inspect registered

restart-celery:
	docker-compose restart visionsworker s3poolerworker celerybeat

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
