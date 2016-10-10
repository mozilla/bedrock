#!/bin/bash
set -ex

DOCKER_CACHE_PATH=~/docker
DOCKER_CACHE_FILE="${DOCKER_CACHE_PATH}/image.tgz"

mkdir -p $DOCKER_CACHE_PATH
make clean

if [[ -f $DOCKER_CACHE_FILE ]]; then
  gunzip -c "$DOCKER_CACHE_FILE" | docker load;
fi

if [[ -f $DOCKER_CACHE_PATH/bedrock.db ]]; then
  mv $DOCKER_CACHE_PATH/bedrock.db ./
fi

LOCALES_TAR_FILE="$DOCKER_CACHE_PATH/locales.tgz"
if [[ -f "$LOCALES_TAR_FILE" ]]; then
  tar xzf "$LOCALES_TAR_FILE"
  rm -f "$LOCALES_TAR_FILE"
fi

MFSA_TAR_FILE="$DOCKER_CACHE_PATH/mfsa_repo.tgz"
if [[ -f "$MFSA_TAR_FILE" ]]; then
  tar xzf "$MFSA_TAR_FILE"
  rm -f "$MFSA_TAR_FILE"
fi

PD_TAR_FILE="$DOCKER_CACHE_PATH/pd_files.tgz"
if [[ -f "$PD_TAR_FILE" ]]; then
  tar xzf "$PD_TAR_FILE"
  rm -f "$PD_TAR_FILE"
fi

if [[ "$CIRCLE_BRANCH" == demo__* ]]; then
  make sync-all
  cp bedrock.db $DOCKER_CACHE_PATH/
  tar czf "$LOCALES_TAR_FILE" locale
  tar czf "$MFSA_TAR_FILE" mofo_security_advisories
  if [[ -d product_details_json ]]; then
    tar czf "$PD_TAR_FILE" product_details_json
  fi
fi

echo "ENV GIT_SHA ${CIRCLE_SHA1}" >> docker/dockerfiles/bedrock_dev_final
make build-final
docker save $(docker history -q bedrock_dev_final | grep -v '<missing>') | gzip > $DOCKER_CACHE_FILE

