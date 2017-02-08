#!/bin/bash
set -ex

# used for pulling from deis
DOCKER_IMAGE_TAG="${DEIS_APP_NAME}:${GIT_COMMIT}"
# used for pushing to registry
PRIVATE_IMAGE_TAG="${PRIVATE_REGISTRY}/${DOCKER_IMAGE_TAG}"

docker tag "mozorg/bedrock_demo:${GIT_COMMIT}" "$PRIVATE_IMAGE_TAG"
docker push "$PRIVATE_IMAGE_TAG"

echo "Creating the demo app $DEIS_APP_NAME"
if deis apps:create "$DEIS_APP_NAME" --no-remote; then
  echo "Configuring the new demo app"
  deis config:push -a "$DEIS_APP_NAME" -p docker/demo.env
  # Sentry DSN is potentially sensitive. Turn off command echo.
  set +x
  if [[ -n "$SENTRY_DEMO_DSN" ]]; then
    deis config:set -a "$DEIS_APP_NAME" "SENTRY_DSN=$SENTRY_DEMO_DSN"
  fi
  set -x
fi
echo "Pulling $DOCKER_IMAGE_TAG into Deis app $DEIS_APP_NAME"
deis pull "$DOCKER_IMAGE_TAG" -a "$DEIS_APP_NAME"
