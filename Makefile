.PHONY: install create_migration_dev install_dev lint migrate run_dev run_prod

install:
	poetry install

install_dev: install
	poetry run pre-commit install

run_dev:
	poetry run app

run_prod: install migrate
	poetry run app

run_all:
	docker compose up -d
	$(MAKE) run_prod

migrate:
	poetry run alembic upgrade head

create_migration_dev:
	@read -p "Введите описание ревизии: " msg; \
	poetry run alembic revision --autogenerate -m "$$msg"

lint:
	poetry run pre-commit run --all
