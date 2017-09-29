#!/bin/bash -xe

# $1 should be the properties name for this run
# defaults
DRIVER=SauceLabs
MARK_EXPRESSION="not headless"

case $1 in
  chrome)
    BROWSER_NAME=chrome
    PLATFORM="Windows 10"
    ;;
  firefox)
    BROWSER_NAME=firefox
    BROWSER_VERSION="45.0"
    PLATFORM="Windows 10"
    ;;
  ie)
    BROWSER_NAME="internet explorer"
    PLATFORM="Windows 10"
    ;;
  ie8)
    BROWSER_NAME="internet explorer"
    BROWSER_VERSION="8.0"
    PLATFORM="Windows 7"
    MARK_EXPRESSION="sanity and not headless"
    ;;
  headless)
    DRIVER=
    MARK_EXPRESSION=headless
    ;;
  smoke)
    DRIVER=Remote
    MARK_EXPRESSION=smoke
    ;;
  *)
    set +x
    echo "Missing or invalid required argument"
    echo
    echo "Usage: run_integration_tests.sh <chrome|firefox|ie{,6,7}|headless|smoke>"
    exit 1
    ;;
esac

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

if [ -z "${BASE_URL}" ]; then
  # start bedrock
  docker run -d --rm \
    --name bedrock-code-${GIT_COMMIT_SHORT} \
    -e ALLOWED_HOSTS="*" \
    -e SECRET_KEY=foo \
    -e DEBUG=False \
    -e DATABASE_URL=sqlite:////tmp/temp.db \
    -e GUNICORN_WORKER_CLASS=sync \
    mozorg/bedrock_code:${GIT_COMMIT} bin/run-for-integration-tests.sh

  DOCKER_LINKS=(--link bedrock-code-${GIT_COMMIT_SHORT}:bedrock)
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
  docker run -d --rm \
    --name bedrock-selenium-hub-${GIT_COMMIT_SHORT} \
    selenium/hub:${SELENIUM_VERSION}
  DOCKER_LINKS=(${DOCKER_LINKS[@]} --link bedrock-selenium-hub-${GIT_COMMIT_SHORT}:hub)
  SELENIUM_HOST="hub"

  # start selenium grid nodes
  for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`; do
    docker run -d --rm \
      --name bedrock-selenium-node-${NODE_NUMBER}-${GIT_COMMIT_SHORT} \
      ${DOCKER_LINKS[@]} \
      selenium/node-firefox:${SELENIUM_VERSION}
    while ! ${SELENIUM_READY}; do
      IP=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' bedrock-selenium-node-${NODE_NUMBER}-${GIT_COMMIT_SHORT}`
      CMD="docker run --rm --link bedrock-selenium-hub-${GIT_COMMIT_SHORT}:hub tutum/curl curl http://hub:4444/grid/api/proxy/?id=http://${IP}:5555 | grep 'proxy found'"
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
docker run --rm -v "${RESULTS_DIR}:${DOCKER_RESULTS_DIR}" -u $(stat -c "%u:%g" "$RESULTS_DIR") \
  ${DOCKER_LINKS[@]} \
  -e "BASE_URL=${BASE_URL}" \
  -e "DRIVER=${DRIVER}" \
  -e "SAUCELABS_USERNAME=${SAUCELABS_USERNAME}" \
  -e "SAUCELABS_API_KEY=${SAUCELABS_API_KEY}" \
  -e "BROWSER_NAME=${BROWSER_NAME}" \
  -e "BROWSER_VERSION=${BROWSER_VERSION}" \
  -e "PLATFORM=${PLATFORM}" \
  -e "SELENIUM_HOST=${SELENIUM_HOST}" \
  -e "SELENIUM_PORT=${SELENIUM_PORT}" \
  -e "SELENIUM_VERSION=${SELENIUM_VERSION}" \
  -e "BUILD_TAG=${BUILD_TAG}" \
  -e "SCREEN_RESOLUTION=${SCREEN_RESOLUTION}" \
  -e "MARK_EXPRESSION=${MARK_EXPRESSION}" \
  -e "TESTS_PATH=${TESTS_PATH}" \
  -e "RESULTS_PATH=${DOCKER_RESULTS_DIR}" \
  -e "PYTEST_PROCESSES=5" \
  -e "PRIVACY=public restricted" \
  mozorg/bedrock_test:${GIT_COMMIT} bin/run-integration-tests.sh
