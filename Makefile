.PHONY: build up down test migrations shell clean

export COMPOSE_REMOVE_ORPHANS=true

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

test:
	@echo "Running test request..."
	@docker-compose run --rm tester sh -c "curl -X POST http://app:8000/users -H 'Content-Type: application/json' -d '{\"name\": \"\u0410\u043b\u0435\u043a\u0441\u0435\u0439\", \"surname\": \"\u0418\u0432\u0430\u043d\u043e\u0432\", \"password\": \"secure123\"}'"

migrations:
	docker-compose run --rm app alembic upgrade head

shell:
	docker-compose exec app /bin/bash

clean:
	docker-compose down -v --rmi local

test-pytest:
	docker-compose run --rm app pytest tests/ -v --tb=long