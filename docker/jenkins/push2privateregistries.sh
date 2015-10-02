#!/bin/bash
# Needs PRIVATE_REGISTRIES, DEIS_APPS,
# FROM_DOCKER_REPOSITORY environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex

# If pull request use $ghprbActualCommit otherwise use $GIT_COMMIT
COMMIT="${ghprbActualCommit:=$GIT_COMMIT}"

# Push to private registry
for PRIVATE_REGISTRY in ${PRIVATE_REGISTRIES//,/ };
do
    for DEIS_APP in ${DEIS_APPS//,/ };
    do
        docker tag -f $FROM_DOCKER_REPOSITORY:$COMMIT $PRIVATE_REGISTRY/$DEIS_APP:$COMMIT
        docker push $PRIVATE_REGISTRY/$DEIS_APP:$COMMIT
    done
done
