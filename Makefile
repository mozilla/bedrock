#TODO: switch to 'git rev-parse --short HEAD'
GIT_COMMIT ?= $(shell git rev-parse HEAD)
VERSION ?= $(shell git describe --tags --exact-match 2>/dev/null || echo ${GIT_COMMIT})
DEV_VERSION ?= latest
REGISTRY ?=
IMAGE_PREFIX ?= mozorg
BASE_IMAGE_NAME ?= bedrock_base
DEV_IMAGE_NAME ?= bedrock_dev
CODE_IMAGE_NAME ?= bedrock_code
L10N_IMAGE_NAME ?= bedrock_l10n
BASE_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/${BASE_IMAGE_NAME}\:${VERSION}
DEV_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/${DEV_IMAGE_NAME}\:${DEV_VERSION}
CODE_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/${CODE_IMAGE_NAME}\:${VERSION}
L10N_IMAGE ?= ${REGISTRY}${IMAGE_PREFIX}/${L10N_IMAGE_NAME}\:${VERSION}
PWD ?= $(shell pwd)
GIT_DIR ?= ${PWD}/.git
DB ?= ${PWD}/bedrock.db
MOUNT_GIT_DB ?= -v ${DB}\:/app/bedrock.db -v ${GIT_DIR}\:/app/.git
MOUNT_APP_DIR ?= -v ${PWD}\:/app 
ENV_FILE ?= .env
PORT ?= 8000
PORT_ARGS ?= -p "${PORT}:${PORT}"
DOCKER_RUN_ARGS ?= --env-file ${ENV_FILE} ${MOUNT_APP_DIR} -w /app
CONTAINER_ID ?= $(shell docker ps --format='{{.ID}}' -f ancestor=${DEV_IMAGE} | head -n 1)
DEIS_APPLICATION ?= bedrock-demo-jgmize
BASE_URL ?= https://www.mozilla.org

env:
	@if [[ ! -e ${ENV_FILE} ]]; then \
		sed -e s/DISABLE_SSL=False/DISABLE_SSL=True/ .bedrock_demo_env > ${ENV_FILE}; \
	fi


help:
	@if [[ -n "$(which rst2ansi)" ]]; then \
		rst2ansi docs/make-commands.rst; \
	else \
		cat docs/make-commands.rst; \
	fi

gulp: env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} gulp

js-lint: env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} gulp js\:lint

unit:
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} ./manage.py test

headless:
	docker run ${DOCKER_RUN_ARGS} -e BASE_URL=${BASE_URL} ${DEV_IMAGE} py.test -m headless

test: unit headless

devserver: env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${DEV_IMAGE} ./manage.py runserver 0.0.0.0\:${PORT}

pull-dev:
	docker pull ${DEV_IMAGE}

codeserver: env
	docker run ${DOCKER_RUN_ARGS} ${PORT_ARGS} ${CODE_IMAGE} ./manage.py runserver 0.0.0.0\:${PORT}

stop:
	docker ps --format={{.ID}} | xargs docker stop

shell_plus: env
	@if [[ -n "${CONTAINER_ID}" ]]; then \
		docker exec -it ${CONTAINER_ID} ./manage.py shell_plus; \
	else \
		docker run -it ${DOCKER_RUN_ARGS} ${DEV_IMAGE} ./manage.py shell_plus; \
	fi

collectstatic: env
	@if [[ -n "${CONTAINER_ID}" ]]; then \
		docker exec -it ${CONTAINER_ID} ./manage.py collectstatic; \
	else \
		docker run -it ${DOCKER_RUN_ARGS} ${DEV_IMAGE} ./manage.py collectstatic --noinput; \
	fi

bash: env
	@if [[ -n "${CONTAINER_ID}" ]]; then \
		docker exec -it ${CONTAINER_ID} bash; \
	else \
		docker run -it ${DOCKER_RUN_ARGS} ${DEV_IMAGE} bash; \
	fi

build-base:
	docker build -f docker/dockerfiles/bedrock_base -t ${BASE_IMAGE} .

build-squash-base:
	docker build -f docker/dockerfiles/bedrock_base -t ${BASE_IMAGE}-tmp .
	docker save ${BASE_IMAGE}-tmp | sudo docker-squash -t ${BASE_IMAGE}-squashed | docker load
	docker tag ${BASE_IMAGE}-squashed ${BASE_IMAGE}

build-dev:
	docker build -f docker/dockerfiles/bedrock_dev -t ${DEV_IMAGE} .

build-code:
	DOCKERFILE=Dockerfile-code-${VERSION}
	FROM_DOCKER_REPOSITORY=mozorg/bedrock_base
	envsubst < docker/dockerfiles/bedrock_code > ${DOCKERFILE}
	docker build -f ${DOCKERFILE} -t ${CODE_IMAGE} .
	rm ${DOCKERFILE}

build-l10n:
	export DOCKER_REPOSITORY=mozorg/bedrock_l10n
	export FROM_DOCKER_REPOSITORY=mozorg/bedrock_code
	./docker/jenkins/include_l10n.sh

push-usw:
	export FROM_DOCKER_REPOSITORY=mozorg/bedrock_l10n
	export PRIVATE_REGISTRIES=localhost:5001
	export DEIS_APPS=${DEIS_APPLICATION}
	./docker/jenkins/push2privateregistries.sh
	DEIS_PROFILE=usw
	deis pull ${DEIS_APPLICATION}:${GIT_COMMIT} -a ${DEIS_APPLICATION}

push-euw:
	export FROM_DOCKER_REPOSITORY=mozorg/bedrock_l10n
	export PRIVATE_REGISTRIES=localhost:5000
	export DEIS_APPS=${DEIS_APPLICATION}
	./docker/jenkins/push2privateregistries.sh
	DEIS_PROFILE=euw
	deis pull ${DEIS_APPLICATION}:${GIT_COMMIT} -a ${DEIS_APPLICATION}

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
