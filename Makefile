.PHONY: all build up down clean

all:
	make build
	make up

build:
	mkdir -p $(HOME)/data/wp
	mkdir -p $(HOME)/data/db
	docker compose -f srcs/docker-compose.yml build

up:
	docker compose -f srcs/docker-compose.yml up

down:
	docker compose -f srcs/docker-compose.yml down

clean:
	docker compose -f srcs/docker-compose.yml down --rmi all --volumes --remove-orphans
