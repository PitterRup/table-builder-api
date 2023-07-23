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
	docker-compose run app poetry run pytest -vv
