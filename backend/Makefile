down:
	docker compose down -v
build:
	docker compose up -d --build

get_backend:
	docker exec -it backend /bin/bash
get_redis:
	docker exec -it redis sh

makemigrations:
	poetry run python manage.py makemigrations
migrate:
	poetry run python manage.py migrate
test:
	poetry run pytest -s .

.PHONY: down,build
.PHONY: get_backend,get_redis
.PHONY: makemigrations,migrate,test
