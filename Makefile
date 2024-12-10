DOMAIN_NAME=$(shell uname -a | awk '{print $$2}')

all:
	make build
	make up

build:
	sed -i "s/^DOMAIN_NAME=.*/DOMAIN_NAME=$(DOMAIN_NAME)/" srcs/.env
	mkdir -p $(HOME)/data/wp
	mkdir -p $(HOME)/data/db
	docker compose -f srcs/docker-compose.yml build

up:
	docker compose -f srcs/docker-compose.yml up

down:
	docker compose -f srcs/docker-compose.yml down

clean:
	docker compose -f srcs/docker-compose.yml down --rmi all --volumes --remove-orphans

.PHONY: all build up down clean