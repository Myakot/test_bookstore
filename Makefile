docker-build:
		docker-compose build

docker-up:
		docker-compose up

docker-down:
		docker-compose down

docker-shell:
		docker-compose run web bash

docker-migrate:
	docker-compose run web python /app/test_bookstore/manage.py migrate