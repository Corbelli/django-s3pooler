#!/bin/bash
.PHONY: default
.SILENT:

default:


shell: 
	docker-compose exec  packageloader bash

build-package:
	docker-compose run --rm packageloader python setup.py sdist

start:
	docker-compose up -d

stop: 
	docker-compose down 

restart:
	docker-compose restart 

build-image:
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
