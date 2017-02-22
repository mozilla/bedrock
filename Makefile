BASE_IMG_NAME = bedrock_base
DEV_IMG_NAME = bedrock_dev
GIT_SHA = $(shell git rev-parse HEAD)
FINAL_IMG_NAME = bedrock_dev_final:${GIT_SHA}

default:
	@echo "You need to specify a subcommand."
	@exit 1

help:
	@echo "build           - build docker containers for dev"
	@echo "run             - docker-compose up the entire system for dev"
	@echo ""
	@echo "clean           - remove all build, test, coverage and Python artifacts"
	@echo "test            - run unit tests"
	@echo "sync-all				 - sync external data to local database"
	@echo "test-image      - run tests on the code built into the docker image"
	@echo "build-final     - build final docker container for demo deployment"
	@echo "docs            - generate Sphinx HTML documentation, including API docs"

.docker-build:
	${MAKE} build

.docker-build-final:
	${MAKE} build-final

build:
	docker build -f docker/dockerfiles/bedrock_base -t ${BASE_IMG_NAME} --pull .
	docker build -f docker/dockerfiles/bedrock_dev -t ${DEV_IMG_NAME} .
	-rm -f .docker-build-final
	touch .docker-build

build-final: .docker-build
	docker build -f docker/dockerfiles/bedrock_dev_final -t ${FINAL_IMG_NAME} .
	touch .docker-build-final

run: .docker-build
	docker run --env-file docker/dev.env -p 8000:8000 -v "$$PWD:/app" ${DEV_IMG_NAME}

django-shell: .docker-build
	docker run --user `id -u` -it --env-file docker/dev.env -v "$$PWD:/app" ${DEV_IMG_NAME} python manage.py shell

shell: .docker-build
	docker run --user `id -u` -it --env-file docker/dev.env -v "$$PWD:/app" ${DEV_IMG_NAME} bash

sync-all: .docker-build
	docker run --user `id -u` --env-file docker/demo.env -v "$$PWD:/app" ${DEV_IMG_NAME} bin/sync_all

clean:
	# python related things
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

	# test related things
	-rm -f .coverage
	-rm -rf results

	# static files
	git clean -fdx static

	# docs files
	-rm -rf docs/_build/

	# state files
	-rm -f .docker-build
	-rm -f .docker-build-final

test: .docker-build
	docker run --user `id -u` --env-file docker/test.env -v "$$PWD:/app" ${DEV_IMG_NAME} docker/run-tests.sh

test-image: .docker-build-final
	docker run --env-file docker/test.env ${FINAL_IMG_NAME} docker/run-tests.sh

docs:
	docker run --user `id -u` --env-file docker/dev.env -v "$$PWD:/app" ${DEV_IMG_NAME} bash -c "make -C docs/ clean && make -C docs/ html"

.PHONY: default clean build build-final docs run test sync-all test-image shell django-shell
