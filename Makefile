.PHONY:install
install:
	poetry install


.PHONY:install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install 


.PHONY: lint
lint:
	poetry run pre-commit run --all-files


.PHONY:migrate
migrate:
	poetry run python -m core.manage migrate


.PHONY:migrations
migrations:
	poetry run python -m core.manage makemigrations


.PHONY:collectstatic
collectstatic:
	poetry run python -m core.manage collectstatic


.PHONY:runserver
runserver:
	poetry run python -m core.manage runserver_plus


.PHONY:superuser
superuser:
	poetry run python -m core.manage createsuperuser


.PHONY:csv-lat-long-addition
csv-lat-long-addition:
	poetry run python -m core.manage csv_lat_long_addition


.PHONY:ml-fuel-price-optimality
ml-fuel-price-optimality:
	poetry run python -m core.manage ml_fuel_price_optimality


.PHONY:unit-test
unit-test:
	poetry run python -m core.manage test --exclude-tag=integration


.PHONY:integrared-test
integrated-test:
	poetry run python -m core.manage test --tag=integration

.PHONY:setup
setup: install migrations migrate install-pre-commit csv-lat-long-addition ml-fuel-price-optimality ;


.PHONY:push-update
push-update: migrations migrate collectstatic ;