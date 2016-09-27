#!/bin/bash
#
set -ex
DOCKER_IMAGE_TAG=${DOCKER_REPOSITORY}:${GIT_COMMIT}
TMP_DOCKER_TAG=${JOB_NAME}${BUILD_NUMBER}

# If docker image exists and no force rebuild do nothing
FORCE_REBUILD=`echo "$FORCE_REBUILD" | tr '[:upper:]' '[:lower:]'`
if [[ $FORCE_REBUILD != "true" ]];
then
    if docker history -q $DOCKER_IMAGE_TAG > /dev/null;
    then
        echo "Docker image already exists, do nothing"
        exit 0;
    fi
fi

cat docker/dockerfiles/${DOCKERFILE} | envsubst > Dockerfile

if [[ $FORCE_REBUILD == "true" ]];
then
    NO_CACHE="true"
fi;

docker build -t ${TMP_DOCKER_TAG} --pull=${UPDATE_DOCKER_IMAGES:-true} --no-cache=${NO_CACHE:-false} . | tee docker-build.log

TAG=`tail -n 1 docker-build.log | awk '{ print $(NF) }'`

if [[ $FORCE_REBUILD != "true" ]];
then
    if tail -n 3 docker-build.log | grep "Using cache";
    then
        echo "Docker image already squashed, skip squashing";
        docker tag ${TAG}-squashed $DOCKER_IMAGE_TAG
        exit 0;
    fi
fi

docker save ${TMP_DOCKER_TAG} | sudo docker-squash -t ${TAG}-squashed | docker load
docker tag ${TAG}-squashed ${DOCKER_IMAGE_TAG}
