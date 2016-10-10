#!/bin/bash
set -e

docker tag bedrock_dev_final "$DOCKER_IMAGE_TAG"

echo "Logging into quay.io"
docker login -e "$QUAY_EMAIL" -u "$QUAY_USERNAME" -p "$QUAY_PASSWORD" quay.io
echo "Pushing ${DOCKER_IMAGE_TAG} to quay.io"
docker push ${DOCKER_IMAGE_TAG}

# Install deis client
echo "Installing Deis client"
curl -sSL http://deis.io/deis-cli/install.sh | sh

DEIS_APP_NAME="bedrock-demo-${CIRCLE_BRANCH#demo__}"
# convert underscores to dashes. Deis does _not_ like underscores.
DEIS_APP_NAME=$( echo "$DEIS_APP_NAME" | tr "_" "-" )
echo "Logging into the Deis Controller at $DEIS_CONTROLLER"
./deis login "$DEIS_CONTROLLER" --username "$DEIS_USERNAME" --password "$DEIS_PASSWORD"
echo "Creating the demo app $DEIS_APP_NAME"
if ./deis apps:create "$DEIS_APP_NAME" --no-remote; then
  echo "Giving github user $CIRCLE_USERNAME perms for the app"
  ./deis perms:create "$CIRCLE_USERNAME" -a "$DEIS_APP_NAME" || true
  echo "Configuring the new demo app"
  ./deis config:push -a "$DEIS_APP_NAME" -p docker/demo.env
  if [[ -n "$SENTRY_DEMO_DSN" ]]; then
    ./deis config:set -a "$DEIS_APP_NAME" "SENTRY_DSN=$SENTRY_DEMO_DSN"
  fi
fi
echo "Pulling $DOCKER_IMAGE_TAG into Deis app $DEIS_APP_NAME"
./deis pull "$DOCKER_IMAGE_TAG" -a "$DEIS_APP_NAME"
