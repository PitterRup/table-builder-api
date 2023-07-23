init:
	cp table_builder_api/table_builder_api/.env.sample table_builder_api/table_builder_api/.env

start:
	docker-compose up -d

start_rebuild:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose down

logs_follow:
	docker-compose logs -f

tests:
	docker-compose run app poetry run pytest -vv $(path)

migrations:
	docker-compose run app poetry run python manage.py makemigrations

migrate:
	docker-compose run app poetry run python manage.py migrate
