#!/bin/bash
set -ex

[[ "$CIRCLE_BRANCH" != demo__* ]] && exit 0

export DOCKER_CACHE_PATH=~/docker

mkdir -p $DOCKER_CACHE_PATH

if [[ -f $DOCKER_CACHE_PATH/bedrock.db ]]; then
  cp $DOCKER_CACHE_PATH/bedrock.db ./
fi

# use settings in manage.py runs
cp .bedrock_demo_env .env

echo "MOFO_SECURITY_ADVISORIES_PATH=$DOCKER_CACHE_PATH/security_advisories" >> .env

./manage.py migrate --noinput
./manage.py rnasync
./manage.py cron update_ical_feeds
./manage.py cron cleanup_ical_events
./manage.py cron update_tweets
./manage.py update_product_details
./manage.py update_externalfiles
./manage.py update_security_advisories
./manage.py runscript update_firefox_os_feeds

cp -f bedrock.db $DOCKER_CACHE_PATH/
# don't include in built container
rm -f .env

if [[ -e $DOCKER_CACHE_PATH/image.tar ]]; then docker load --input $DOCKER_CACHE_PATH/image.tar; fi
echo "ENV GIT_SHA ${CIRCLE_SHA1}" >> Dockerfile
docker build -t "$DOCKER_IMAGE_TAG" --pull=true .
docker save "$DOCKER_IMAGE_TAG" > $DOCKER_CACHE_PATH/image.tar
