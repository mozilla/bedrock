#!/bin/bash
#
# Starts Selenium Hub and NUMBER_OF_NODES (default 5) firefox nodes.
# Waits until at least one node is ready and then runs smoke tests
# only against a local bedrock instance started for this job.
#
set -xe

SELENIUM_VERSION=${SELENIUM_VERSION:-2.48.2}
GIT_COMMIT=${GIT_COMMIT:-$(git rev-parse HEAD)}

cp docker/dockerfiles/bedrock_functional_tests Dockerfile
docker build -t bedrock_functional_tests:$GIT_COMMIT --pull=true .

docker pull selenium/hub:${SELENIUM_VERSION}
docker pull selenium/node-firefox:${SELENIUM_VERSION}

docker run -d --name bedrock-code-${BUILD_NUMBER} -e ALLOWED_HOSTS="*" -e SECRET_KEY=foo -e DEBUG=False -e DATABASE_URL=sqlite:////tmp/temp.db mozorg/bedrock_code:$GIT_COMMIT
docker run -d --name bedrock-selenium-hub-${BUILD_NUMBER} selenium/hub:${SELENIUM_VERSION}

for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`;
do
    docker run -d --name bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER} --link bedrock-selenium-hub-${BUILD_NUMBER}:hub --link bedrock-code-${BUILD_NUMBER}:bedrock selenium/node-firefox:${SELENIUM_VERSION}
done;

SELENIUM_READY=false
while ! ${SELENIUM_READY};
do
    for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`;
    do
        IP=`docker inspect --format '{{ .NetworkSettings.IPAddress }}' bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER}`
        CMD="docker run --link bedrock-selenium-hub-${BUILD_NUMBER}:hub tutum/curl curl http://hub:4444/grid/api/proxy/?id=http://${IP}:5555 | grep 'proxy found'"
        if eval ${CMD};
        then
            SELENIUM_READY=true
        fi;
    done;
done;

docker run -v `pwd`/results:/app/results \
  --link bedrock-selenium-hub-${BUILD_NUMBER}:hub \
  --link bedrock-code-${BUILD_NUMBER}:bedrock \
  -e SELENIUM_HOST=hub \
  -e BASE_URL=http://bedrock:8000 \
  -e MARK_EXPRESSION=${MARK_EXPRESSION} \
  bedrock_functional_tests:$GIT_COMMIT
