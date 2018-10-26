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

start-prod:
	docker-compose -f docker-compose.prod.yml up -d

stop-prod: _local_env
	docker-compose -f docker-compose.prod.yml down -v

stop-d:
	docker-compose stop django

start-d:
	docker-compose start django

django:
	clear
	docker-compose logs -f --tail=1  django

stop: _local_env
	docker-compose down 

restart:
	docker-compose restart django

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
