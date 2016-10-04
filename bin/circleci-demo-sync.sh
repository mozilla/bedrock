#!/bin/bash
set -ex

[[ "$CIRCLE_BRANCH" != demo__* ]] && exit 0

export DOCKER_CACHE_PATH=~/docker

mkdir -p $DOCKER_CACHE_PATH

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

# use settings in manage.py runs
cp .bedrock_demo_env .env

./manage.py migrate --noinput --database bedrock
./manage.py l10n_update
./manage.py rnasync
./manage.py cron update_ical_feeds
./manage.py cron cleanup_ical_events
./manage.py cron update_tweets
./manage.py update_product_details --database bedrock
./manage.py update_blog_feeds --database bedrock
./manage.py update_externalfiles
./manage.py update_security_advisories
./manage.py runscript update_firefox_os_feeds

cp bedrock.db $DOCKER_CACHE_PATH/
tar czf "$LOCALES_TAR_FILE" locale
tar czf "$MFSA_TAR_FILE" mofo_security_advisories
# don't include in built container
rm -f .env

if [[ -e $DOCKER_CACHE_PATH/image.tar ]]; then docker load --input $DOCKER_CACHE_PATH/image.tar; fi
echo "ENV GIT_SHA ${CIRCLE_SHA1}" >> Dockerfile
docker build -t "$DOCKER_IMAGE_TAG" --pull=true .
docker save "$DOCKER_IMAGE_TAG" > $DOCKER_CACHE_PATH/image.tar
