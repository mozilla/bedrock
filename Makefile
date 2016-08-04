SHELL := /bin/bash --init-file make_functions.sh -i
BEDROCK_COMMIT ?= $(shell git rev-parse --short HEAD)
LATEST_TAGGED_COMMIT ?= $(shell git rev-parse --short ${LATEST_TAG}~0)
DEV_VERSION ?= latest
REGISTRY ?=
EUW_REGISTRY ?= localhost:5000
USW_REGISTRY ?= localhost:5001
TAG_PREFIX ?=
IMAGE_PREFIX ?= mozorg
DEV_IMAGE_NAME ?= bedrock_dev
L10N_REPO ?= "https://github.com/mozilla-l10n/bedrock-l10n"
L10N_DEV ?=
L10N_DEV_REPO ?= "https://github.com/mozilla-l10n/www.mozilla.org"
L10N_COMMIT ?= $(shell cd locale && git rev-parse --short HEAD)
DEV_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/${DEV_IMAGE_NAME}:${DEV_VERSION}
BASE_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/bedrock_base:${TAG_PREFIX}${BEDROCK_COMMIT}
DEPLOY_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/bedrock:${TAG_PREFIX}${BEDROCK_COMMIT}-${L10N_COMMIT}
DEV_DOCKERFILE ?= docker/dockerfiles/bedrock_dev
BASE_DOCKERFILE ?= docker/dockerfiles/bedrock_base
DEPLOY_DOCKERFILE ?= docker/dockerfiles/bedrock_deploy-${BEDROCK_COMMIT}
DOCKERFILE ?= ${BASE_DOCKERFILE}
IMAGE ?= ${BASE_IMAGE}
PWD ?= $(shell pwd)
GIT_DIR ?= ${PWD}/.git
DB ?= ${PWD}/bedrock.db
MOUNT_GIT_DB ?= -v "${DB}:/app/bedrock.db" -v "${GIT_DIR}:/app/.git"
MOUNT_APP_DIR ?= -v "${PWD}:/app"
ENV_FILE ?= .env
PORT ?= 8000
PORT_ARGS ?= -p "${PORT}:${PORT}"
UID_ARGS ?= -u "$(shell id -u):$(shell id -g)"
DOCKER_RUN_ARGS ?= --env-file ${ENV_FILE} ${MOUNT_APP_DIR} -w /app ${UID_ARGS}
CONTAINER_ID ?= $(shell docker ps --format='{{.ID}}' -f ancestor=${DEV_IMAGE} | head -n 1)
DEIS_APP_NAME ?= bedrock-demo-jgmize
DEIS_PULL ?= "${DEIS_APP_NAME}:${TAG_PREFIX}${BEDROCK_COMMIT}-${L10N_COMMIT}"
BASE_URL ?= "https://www.mozilla.org"
COLLECTSTATIC ?= "./manage.py collectstatic -l -v 0 --noinput && ./bin/softlinkstatic.py"

.env:
	sed -e s/DISABLE_SSL=False/DISABLE_SSL=True/ .bedrock_demo_env | egrep -v "^DEV=" > .env


help:
	@if [ -n "$(which rst2ansi)" ]; then \
		rst2ansi docs/make-commands.rst; \
	else \
		cat docs/make-commands.rst; \
	fi

gulp: .env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} gulp

js-lint: .env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} gulp js\:lint

unit: .env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} py.test lib bedrock

headless:
	docker run ${DOCKER_RUN_ARGS} -e BASE_URL=${BASE_URL} ${DEV_IMAGE} py.test -m headless

test: unit headless

devserver: .env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} ./manage.py runserver 0.0.0.0\:${PORT}

pull-dev:
	docker pull ${DEV_IMAGE}

push-dev-dockerhub:
	docker push ${DEV_IMAGE}

stop:
	docker ps --format={{.ID}} | xargs docker stop

shell_plus: .env
	@if [ -n "${CONTAINER_ID}" ]; then \
		docker exec -it ${CONTAINER_ID} ./manage.py shell_plus; \
	else \
		docker run -it ${DOCKER_RUN_ARGS} ${DEV_IMAGE} ./manage.py shell_plus; \
	fi

collectstatic: .env
	@if [ -n "${CONTAINER_ID}" ]; then \
		docker exec ${CONTAINER_ID} bash -c ${COLLECTSTATIC}; \
	else \
		docker run ${DOCKER_RUN_ARGS} ${DEV_IMAGE} bash -c ${COLLECTSTATIC}; \
	fi

bash: .env
	@if [ -n "${CONTAINER_ID}" ]; then \
		docker exec -it ${CONTAINER_ID} bash; \
	else \
		docker run -it ${DOCKER_RUN_ARGS} ${DEV_IMAGE} bash; \
	fi

build-squash:
	docker build -f ${DOCKERFILE} -t ${IMAGE}-tmp . | tee docker-build.log
	if [ -n "$(shell tail -n 3 docker-build.log | grep 'Using cache')" ]; then \
		docker tag -f $(shell tail -n 1 docker-build.log | awk '{ print $$(NF) }') ${IMAGE}-squashed; \
	else \
		docker save ${IMAGE}-tmp | sudo docker-squash -t ${IMAGE}-squashed | docker load; \
	fi
	docker tag ${IMAGE}-squashed ${IMAGE}

build-base:
	if [ -z "$(shell docker images -q ${BASE_IMAGE})" ]; then \
		make build-squash IMAGE=${BASE_IMAGE} DOCKERFILE=${BASE_DOCKERFILE}; \
	fi

build-dev:
	docker build -f ${DEV_DOCKERFILE} -t ${DEV_IMAGE} .

locale:
	if [ -n "${L10N_DEV}" ]; then \
		git clone --depth 1 ${L10N_DEV_REPO} locale; \
	else \
		git clone --depth 1 ${L10N_REPO} locale; \
	fi

update-locale: locale
	bash -c "cd locale && git fetch origin && git checkout -f origin/master"

build-deploy: build-base collectstatic update-locale
	docker run ${MOUNT_APP_DIR} -e BASE_IMAGE=${BASE_IMAGE} ${DEV_IMAGE} bash -c \
	"envsubst < docker/dockerfiles/bedrock_deploy" > ${DEPLOY_DOCKERFILE}-${BEDROCK_COMMIT}
	make build-squash DOCKERFILE=${DEPLOY_DOCKERFILE}-${BEDROCK_COMMIT} IMAGE=${DEPLOY_IMAGE}
	rm ${DEPLOY_DOCKERFILE}-${BEDROCK_COMMIT}

build-deploy-demo:
	make build-deploy TAG_PREFIX=demo-
	create-deis-app
	make push-usw TAG_PREFIX=demo-

push-usw:
	docker tag -f ${DEPLOY_IMAGE} ${USW_REGISTRY}/${DEIS_PULL}
	docker push ${USW_REGISTRY}/${DEIS_PULL}
	DEIS_PROFILE=usw deis pull ${DEIS_PULL} -a ${DEIS_APP_NAME}

push-euw:
	docker tag -f ${DEPLOY_IMAGE} ${EUW_REGISTRY}/${DEIS_PULL}
	docker push ${EUW_REGISTRY}/${DEIS_PULL}
	DEIS_PROFILE=euw deis pull ${DEIS_PULL} -a ${DEIS_APP_NAME}

media-change:
	@if [ -n "${MEDIA_PATH}" ]; then \
		cp ${MEDIA_PATH} $(subst /media/,/static/,${MEDIA_PATH}); \
		if [ -n "$(filter %.js,${MEDIA_PATH})" ]; then \
			make js-lint; \
		fi \
	fi

brew-fswatch:
	@if [ -z "$(which fswatch)" ]; then \
		if [ -z "$(which brew)" ]; then \
			/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"; \
		fi; \
		brew install fswatch; \
	fi

fswatch-media:
	fswatch -0 media | xargs -0 -n 1 -I {} make media-change MEDIA_PATH={}

webhook-dispatch:
	GIT_BRANCH=${GIT_BRANCH} check-branch-commit
	check-tag
