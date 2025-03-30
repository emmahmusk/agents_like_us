export PIPENV_IGNORE_VIRTUALENVS=1

.PHONY: docker/build
docker/build:
	docker build -f ./Dockerfile -t tracr-ai:latest .

.PHONY: tidy
tidy:
	pipenv run autoflake --in-place --remove-all-unused-imports -r --exclude migrations ./src
	pipenv run isort --atomic ./src/
	pipenv run black ./src/ --exclude=migrations

.PHONY: run
run:
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate
	pipenv run python manage.py runserver