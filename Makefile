include .env
DOCKER_COMPOSE=docker compose -f docker-compose.yml

all: 
	mkdir -p ./data/postgresql
	mkdir -p ./data/minio
	mkdir -p ./secrets/
	@if [ ! -f ./secrets/db_password.txt ]; then \
		echo $(POSTGRES_DB) > ./secrets/db_password.txt; \
	fi
	$(DOCKER_COMPOSE) up -d postgres minio
	$(DOCKER_COMPOSE) build api-extractor
	$(DOCKER_COMPOSE) run --rm api-extractor

clean:
	$(DOCKER_COMPOSE) down

.PHONY: all clean