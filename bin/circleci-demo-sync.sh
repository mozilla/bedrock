#!/bin/bash
set -ex

[[ "$CIRCLE_BRANCH" != demo__* ]] && exit 0

DATABASE_URL=sqlite:///bedrock.db
DOCKER_CACHE_PATH=~/docker
MOFO_SECURITY_ADVISORIES_PATH=$DOCKER_CACHE_PATH/security_advisories

mkdir -p $DOCKER_CACHE_PATH

if [[ -f $DOCKER_CACHE_PATH/bedrock.db ]]; then
  cp $DOCKER_CACHE_PATH/bedrock.db ./
fi

./manage.py migrate --noinput
./manage.py rnasync
./manage.py cron update_ical_feeds
./manage.py update_product_details
./manage.py update_externalfiles
./manage.py update_security_advisories

cp -f bedrock.db $DOCKER_CACHE_PATH/

if [[ -e $DOCKER_CACHE_PATH/image.tar ]]; then docker load --input ~/docker/image.tar; fi
echo "ENV GIT_SHA ${CIRCLE_SHA1}" >> Dockerfile
docker build -t "$DOCKER_IMAGE_TAG" --pull=true .
docker save "$DOCKER_IMAGE_TAG" > $DOCKER_CACHE_PATH/image.tar
