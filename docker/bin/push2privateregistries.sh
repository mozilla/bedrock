#!/bin/bash
# Needs PRIVATE_REGISTRIES, DEIS_APPS,
# FROM_DOCKER_REPOSITORY environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#
set -ex


FROM_DOCKER_REPOSITORY='mozorg/bedrock_l10n'
DOCKER_TAG="${BRANCH_NAME/\//-}-${GIT_COMMIT}"

# Push to private registry
for PRIVATE_REGISTRY in ${PRIVATE_REGISTRIES//,/ };
do
    for DEIS_APP in ${DEIS_APPS//,/ };
    do
        docker tag $FROM_DOCKER_REPOSITORY:${DOCKER_TAG} $PRIVATE_REGISTRY/$DEIS_APP:${GIT_COMMIT}
        docker push $PRIVATE_REGISTRY/$DEIS_APP:${GIT_COMMIT}
    done
done
