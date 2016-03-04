#!/bin/bash
set -e

echo "Logging into the Docker Hub"
docker login -e "$DOCKER_EMAIL" -u "$DOCKER_USERNAME" -p "$DOCKER_PASSWORD"
echo "Pushing ${DOCKER_IMAGE_TAG} to Docker hub"
docker push ${DOCKER_IMAGE_TAG}

# Install deis client
echo "Installing Deis client"
curl -sSL http://deis.io/deis-cli/install.sh | sh

DEIS_APP_NAME="bedrock-demo-${CIRCLE_BRANCH#demo__}"
echo "Logging into the Deis Controller at $DEIS_CONTROLLER"
./deis login "$DEIS_CONTROLLER" --username "$DEIS_USERNAME" --password "$DEIS_PASSWORD"
echo "Creating the demo app $DEIS_APP_NAME"
if ./deis apps:create "$DEIS_APP_NAME" --no-remote; then
  echo "Giving github user $CIRCLE_USERNAME perms for the app"
  ./deis perms:create "$CIRCLE_USERNAME" -a "$DEIS_APP_NAME" || true
  echo "Configuring the new demo app"
  ./deis config:push -a "$DEIS_APP_NAME" -p .bedrock_demo_env
fi
echo "Pulling $DOCKER_IMAGE_TAG into Deis app $DEIS_APP_NAME"
./deis pull "$DOCKER_IMAGE_TAG" -a "$DEIS_APP_NAME"
