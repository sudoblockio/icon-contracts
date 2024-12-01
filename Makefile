.PHONY: test help

test: up-dbs test-unit test-integration

up-dbs:  ## Bring up the DBs
	docker compose -f docker-compose.db.yml up -d
	sleep 5
	cd icon_contracts && PYTHONPATH=$PYTHONPATH:`pwd`/.. alembic upgrade head

down-dbs:  ## Take down the DBs
	docker compose -f docker-compose.db.yml down

test-unit:  ## Run unit tests
	python3 -m pytest tests/unit

test-integration:  ## Run integration tests - Need DB compose up
	python3 -m pytest tests/integration

test-coverage:  ## Run unit tests - Need DB compose up
	PYTHONPATH=$PYTHONPATH:`pwd` pytest --cov=icon_contracts --cov-report xml tests/integration
	PYTHONPATH=$PYTHONPATH:`pwd` pytest --cov=icon_contracts --cov-append --cov-report xml tests/unit

up:  ## Bring everything up as containers
	docker compose -f docker-compose.db.yml -f docker-compose.yml up -d

down:  ## Take down all the containers
	docker compose -f docker-compose.db.yml -f docker-compose.yml down

clean:
	docker volume rm $(docker volume ls -q)

build:  ## Build everything
	docker compose build

ps:  ## List all containers and running status
	docker compose -f docker-compose.db.yml -f docker-compose.yml ps

postgres-console:  ## Start postgres terminal
	docker compose -f docker-compose.db.yml -f docker-compose.yml exec postgres psql -U postgres

install:  ## Install requirements
	pip install -r requirements_api.txt -r requirements_worker.txt -r requirements_dev.txt

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'
