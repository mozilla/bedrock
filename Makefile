DC_CI = "bin/docker-compose.sh"
DC = $(shell which docker-compose)

default: help
	@echo ""
	@echo "You need to specify a subcommand."
	@exit 1

help:
	@echo "build         - build docker images for dev"
	@echo "run           - docker-compose up the entire system for dev"
	@echo ""
	@echo "pull          - pull the latest production images from Docker Hub"
	@echo "shell         - start the Django Python shell (bpython and shell_plus)"
	@echo "clean         - remove all build, test, coverage and Python artifacts"
	@echo "rebuild       - force a rebuild of all of the docker images"
	@echo "submodules    - resync and fetch the latest git submodules"
	@echo "lint          - check style with flake8, jshint, and stylelint"
	@echo "test          - run tests against local files"
	@echo "test-image    - run tests against files in docker image"
	@echo "docs          - generate Sphinx HTML documentation"
	@echo "build-ci      - build docker images for use in our CI pipeline"
	@echo "test-ci       - run tests against files in docker image built by CI"

.env:
	@if [ ! -f .env ]; then \
		echo "Copying .env-dist to .env..."; \
		cp .env-dist .env; \
	fi

.docker-build:
	${MAKE} build

.docker-build-pull:
	${MAKE} pull

build: .docker-build-pull
	${DC} build app assets
	touch .docker-build

pull: .env submodules
	-GIT_COMMIT= ${DC} pull release app assets builder app-base
	touch .docker-build-pull

rebuild: clean build

run: .docker-build-pull
	${DC} up assets app

submodules:
	git submodule sync
	git submodule update -f --init --recursive

shell: .docker-build-pull
	${DC} run app python manage.py shell_plus

clean:
#	python related things
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +
#	test related things
	-rm -f .coverage
#	docs files
	-rm -rf docs/_build/
#	static files
	-rm -rf static_build/
#	state files
	-rm -f .docker-build*

lint: .docker-build-pull
	${DC} run test flake8 bedrock lib tests
	${DC} run assets gulp js:lint css:lint

test: .docker-build-pull
	${DC} run test

test-image: .docker-build
	${DC} run test-image

docs: .docker-build-pull
	${DC} run app make -C docs/ clean html

###############
# For use in CI
###############
.docker-build-ci:
	${MAKE} build-ci

build-ci: .docker-build-pull
	${DC_CI} build release
#	tag intermediate images using cache
	${DC_CI} build app assets builder app-base
	touch .docker-build-ci

test-ci: .docker-build-ci
	${DC_CI} run test-image

.PHONY: default clean build pull submodules docs lint run shell test test-image rebuild build-ci test-ci
