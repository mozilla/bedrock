#!/bin/bash -xe
GIT_COMMIT=${GIT_COMMIT:-$(git rev-parse HEAD)}
cp docker/dockerfiles/bedrock_functional_tests Dockerfile
docker build -t bedrock_functional_tests:${GIT_COMMIT} --pull=true .

if [ "${DRIVER}" = "Remote" ]; then
  # Start Selenium hub and NUMBER_OF_NODES (default 5) firefox nodes.
  # Waits until all nodes are ready and then runs tests against a local
  # bedrock instance.

  SELENIUM_VERSION=${SELENIUM_VERSION:-2.48.2}

  docker pull selenium/hub:${SELENIUM_VERSION}
  docker pull selenium/node-firefox:${SELENIUM_VERSION}

  # start bedrock
  docker run -d \
    --name bedrock-code-${BUILD_NUMBER} \
    -e ALLOWED_HOSTS="*" \
    -e SECRET_KEY=foo \
    -e DEBUG=False \
    -e DATABASE_URL=sqlite:////tmp/temp.db \
    mozorg/bedrock_code:$GIT_COMMIT

  # start selenium grid hub
  docker run -d \
    --name bedrock-selenium-hub-${BUILD_NUMBER} \
    selenium/hub:${SELENIUM_VERSION}

  # start selenium grid nodes
  for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`; do
    docker run -d \
      --name bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER} \
      --link bedrock-selenium-hub-${BUILD_NUMBER}:hub \
      --link bedrock-code-${BUILD_NUMBER}:bedrock \
      selenium/node-firefox:${SELENIUM_VERSION}
    while ! ${SELENIUM_READY}; do
      IP=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER}`
      CMD="docker run --link bedrock-selenium-hub-${BUILD_NUMBER}:hub tutum/curl curl http://hub:4444/grid/api/proxy/?id=http://${IP}:5555 | grep 'proxy found'"
      if eval ${CMD}; then SELENIUM_READY=true; fi
    done
  done

  docker run -v `pwd`/results:/app/results \
    --link bedrock-selenium-hub-${BUILD_NUMBER}:hub \
    --link bedrock-code-${BUILD_NUMBER}:bedrock \
    -e BASE_URL=http://bedrock:8000 \
    -e DRIVER=${DRIVER} \
    -e SELENIUM_HOST=hub \
    -e MARK_EXPRESSION=${MARK_EXPRESSION} \
    bedrock_functional_tests:$GIT_COMMIT
else
  # Runs functional tests that either don't require Selenium, use a local
  # Selenium driver, or use a remote Selenium server (such as Sauce Labs).
  docker run -v `pwd`/results:/app/results \
    -e BASE_URL=${BASE_URL} \
    -e DRIVER=${DRIVER} \
    -e SAUCELABS_USERNAME=${SAUCELABS_USERNAME} \
    -e SAUCELABS_API_KEY=${SAUCELABS_API_KEY} \
    -e BROWSER_NAME="${BROWSER_NAME}" \
    -e BROWSER_VERSION=${BROWSER_VERSION} \
    -e PLATFORM="${PLATFORM}" \
    -e SELENIUM_VERSION=${SELENIUM_VERSION} \
    -e BUILD_TAG=${BUILD_TAG} \
    -e SCREEN_RESOLUTION=${SCREEN_RESOLUTION} \
    -e MARK_EXPRESSION="${MARK_EXPRESSION}" \
    bedrock_functional_tests:${GIT_COMMIT}
fi
