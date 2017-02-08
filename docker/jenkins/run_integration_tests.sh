#!/bin/bash -xe

# $1 should be the properties file for this run
source "docker/jenkins/properties/integration_tests/${1}.properties"

if [[ -z "$GIT_COMMIT" ]]; then
  GIT_COMMIT=$(git rev-parse HEAD)
fi

BUILD_NUMBER="${BUILD_NUMBER:-0}"

if [ -z "${BASE_URL}" ]; then
  # start bedrock
  docker run -d \
    --name bedrock-code-${BUILD_NUMBER} \
    -e ALLOWED_HOSTS="*" \
    -e SECRET_KEY=foo \
    -e DEBUG=False \
    -e DATABASE_URL=sqlite:////tmp/temp.db \
    mozorg/bedrock_code:${GIT_COMMIT}

  DOCKER_LINKS=(--link bedrock-code-${BUILD_NUMBER}:bedrock)
  BASE_URL="http://bedrock:8000"
fi

if [ "${DRIVER}" = "Remote" ]; then
  # Start Selenium hub and NUMBER_OF_NODES (default 5) firefox nodes.
  # Waits until all nodes are ready and then runs tests against a local
  # bedrock instance.

  SELENIUM_VERSION=${SELENIUM_VERSION:-2.48.2}

  docker pull selenium/hub:${SELENIUM_VERSION}
  docker pull selenium/node-firefox:${SELENIUM_VERSION}

  # start selenium grid hub
  docker run -d \
    --name bedrock-selenium-hub-${BUILD_NUMBER} \
    selenium/hub:${SELENIUM_VERSION}
  DOCKER_LINKS=(${DOCKER_LINKS[@]} --link bedrock-selenium-hub-${BUILD_NUMBER}:hub)
  SELENIUM_HOST="hub"

  # start selenium grid nodes
  for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`; do
    docker run -d \
      --name bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER} \
      ${DOCKER_LINKS[@]} \
      selenium/node-firefox:${SELENIUM_VERSION}
    while ! ${SELENIUM_READY}; do
      IP=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER}`
      CMD="docker run --link bedrock-selenium-hub-${BUILD_NUMBER}:hub tutum/curl curl http://hub:4444/grid/api/proxy/?id=http://${IP}:5555 | grep 'proxy found'"
      if eval ${CMD}; then SELENIUM_READY=true; fi
    done
  done
fi

# make sure results dir exists or docker will create it
# and it will be owned by root
RESULTS_DIR="$PWD/results"
DOCKER_RESULTS_DIR="/app/results"
rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"
docker run -v "${RESULTS_DIR}:${DOCKER_RESULTS_DIR}" -u $(stat -c "%u:%g" "$RESULTS_DIR") \
  ${DOCKER_LINKS[@]} \
  -e BASE_URL=${BASE_URL} \
  -e DRIVER=${DRIVER} \
  -e SAUCELABS_USERNAME=${SAUCELABS_USERNAME} \
  -e SAUCELABS_API_KEY=${SAUCELABS_API_KEY} \
  -e BROWSER_NAME="${BROWSER_NAME}" \
  -e BROWSER_VERSION=${BROWSER_VERSION} \
  -e PLATFORM="${PLATFORM}" \
  -e SELENIUM_HOST=${SELENIUM_HOST} \
  -e SELENIUM_PORT=${SELENIUM_PORT} \
  -e SELENIUM_VERSION=${SELENIUM_VERSION} \
  -e BUILD_TAG=${BUILD_TAG} \
  -e SCREEN_RESOLUTION=${SCREEN_RESOLUTION} \
  -e MARK_EXPRESSION="${MARK_EXPRESSION}" \
  -e TESTS_PATH="${TESTS_PATH}" \
  -e RESULTS_PATH="${DOCKER_RESULTS_DIR}" \
  -e PYTEST_PROCESSES=5 \
  -e PRIVACY="public restricted" \
  mozorg/bedrock_test:${GIT_COMMIT} bin/run-integration-tests.sh
