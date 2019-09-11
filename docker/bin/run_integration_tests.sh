#!/bin/bash -xe

# $1 should be the properties name for this run
# defaults
DRIVER=SauceLabs
MARK_EXPRESSION="not headless and not download"

case $1 in
  chrome)
    BROWSER_NAME=chrome
    PLATFORM="Windows 10"
    ;;
  firefox)
    BROWSER_NAME=firefox
    BROWSER_VERSION="57.0"
    PLATFORM="Windows 10"
    ;;
  ie)
    BROWSER_NAME="internet explorer"
    PLATFORM="Windows 10"
    ;;
  ie9)
    BROWSER_NAME="internet explorer"
    BROWSER_VERSION="9.0"
    PLATFORM="Windows 7"
    MARK_EXPRESSION=sanity
    ;;
  download)
    DRIVER=
    MARK_EXPRESSION=download
    ;;
  headless)
    DRIVER=
    MARK_EXPRESSION=headless
    ;;
  *)
    set +x
    echo "Missing or invalid required argument"
    echo
    echo "Usage: run_integration_tests.sh <chrome|firefox|ie{,6,7}|headless>"
    exit 1
    ;;
esac

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

if [ -z "${BASE_URL}" ]; then
  # start bedrock
  docker run -d --rm \
    --name bedrock-code-${BRANCH_AND_COMMIT} \
    --env-file docker/envfiles/prod.env \
    ${DEPLOYMENT_DOCKER_IMAGE} bin/run-prod.sh

  DOCKER_LINKS=(--link bedrock-code-${BRANCH_AND_COMMIT}:bedrock)
  BASE_URL="http://bedrock:8000"
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
