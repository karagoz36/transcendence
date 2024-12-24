DOMAIN_NAME=$(shell uname -a | awk '{print $$2}')

all:
	make build
	make up

test:
	cp srcs/.env.template srcs/.env
	docker compose -f srcs/docker-compose.yml build
	docker compose -f srcs/docker-compose.yml up -d
	docker exec django python /app/manage.py test unittests.tests

build:
	sed -i '' "s/^DOMAIN_NAME=.*/DOMAIN_NAME=$(DOMAIN_NAME)/" srcs/.env
	docker compose -f srcs/docker-compose.yml build

up:
	docker compose -f srcs/docker-compose.yml up

down:
	docker compose -f srcs/docker-compose.yml down

clean:
	docker compose -f srcs/docker-compose.yml down --rmi all --volumes --remove-orphans

.PHONY: all build up down clean
