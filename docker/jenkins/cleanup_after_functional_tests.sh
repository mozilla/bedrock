#!/bin/bash -x

BUILD_NUMBER="${BUILD_NUMBER:-0}"

docker stop bedrock-code-${BUILD_NUMBER}
docker rm bedrock-code-${BUILD_NUMBER}

for NODE_NUMBER in `seq ${NUMBER_OF_NODES:-5}`;
do
    docker stop bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER}
    docker rm bedrock-selenium-node-${NODE_NUMBER}-${BUILD_NUMBER}
done;

docker stop bedrock-selenium-hub-${BUILD_NUMBER}
docker rm bedrock-selenium-hub-${BUILD_NUMBER}

# always report success
exit 0
