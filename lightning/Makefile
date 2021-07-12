.PHONY: init init-migration build run db-migrate test tox

init:  build
	docker-compose run --rm webservice flask db init
	docker-compose run --rm webservice flask db migrate
	docker-compose run --rm webservice flask db upgrade
	docker-compose run --rm webservice flask admin create-admin
	@echo "Init done, containers running"

build:
	docker-compose build

db-migrate:
	docker-compose run --rm webservice flask db migrate

db-upgrade:
	docker-compose run --rm webservice flask db upgrade

test:
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker-compose run -v $(PWD)/tests:/code/tests:ro webservice tox -e test
	docker-compose start celery

tox:
	docker-compose stop celery # stop celery to avoid conflicts with celery tests
	docker-compose start rabbitmq redis # ensuring both redis and rabbitmq are started
	docker-compose run -v $(PWD)/tests:/code/tests:ro webservice tox -e py38
	docker-compose start celery

lint:
	docker-compose run webservice tox -e lint
