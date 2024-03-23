down:
	docker compose down -v
build:
	docker compose up -d --build

get_backend:
	docker exec -it backend /bin/bash
get_redis:
	docker exec -it redis sh

run_server:
	poetry run python manage.py runserver
create_superuser:
	poetry run python manage.py createsuperuser

test:
	poetry run pytest -s .
test_paralel:
	poetry run pytest -n auto

run_migrate:
	poetry run python manage.py migrate
run_makemigrations:
	poetry run python manage.py makemigrations
run_migrations:
	bash run_migrations.sh
clean_migrations:
	bash clean_migrations.sh

install:
	poetry install

.PHONY: down,build
.PHONY: get_backend,get_redis
.PHONY: run_server,create_superuser
.PHONY: test, test_paralel
.PHONY: run_makemigrations,run_migrate,run_migrations,clean_migrations
.PHONY: install
