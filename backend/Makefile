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

run_migrations:
	bash run_migrations.sh
clean_migrations:
	bash clean_migrations.sh

.PHONY: down,build
.PHONY: get_backend,get_redis
.PHONY: test create_superuser
.PHONY: run_migrations,clean_migrations
