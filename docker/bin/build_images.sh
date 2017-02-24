#!/bin/bash

set -exo pipefail

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

BUILD_IMAGE_TAG="mozorg/bedrock_build:${GIT_COMMIT}"
CODE_IMAGE_TAG="mozorg/bedrock_code:${GIT_COMMIT}"
DOCKER_REBUILD=false
# demo mode will build the demo image containing a db file full of data
DEMO_MODE=false
# prod mode will build the l10n image containing the locale dir
PROD_MODE=false
# test mode will build the unit testing image containing the testing requirements
TEST_MODE=false

# parse cli args
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -r|--rebuild)
            DOCKER_REBUILD=true
            ;;
        -d|--demo)
            DEMO_MODE=true
            ;;
        -p|--prod)
            PROD_MODE=true
            ;;
        -t|--test)
            TEST_MODE=true
            ;;
    esac
    shift # past argument or value
done

function imageExists() {
    if $DOCKER_REBUILD; then
        return 1
    fi
    if [[ "$1" == "l10n" ]]; then
        DOCKER_TAG="${BRANCH_NAME}-${GIT_COMMIT}"
    else
        DOCKER_TAG="${GIT_COMMIT}"
    fi
    docker history -q "mozorg/bedrock_${1}:${DOCKER_TAG}" > /dev/null 2>&1
    return $?
}

function dockerRun() {
    env_file="$1"
    image_tag="mozorg/bedrock_${2}:${GIT_COMMIT}"
    cmd="$3"
    docker run --user $(id -u) -v "$PWD:/app" --env-file "docker/envfiles/${env_file}.env" "$image_tag" bash -c "$cmd"
}

if ! imageExists "base"; then
    docker/bin/docker_build.sh --pull "base"
fi

# build the static files using the builder image
# and include those and the app in a code image
if ! imageExists "code"; then
    # build a staticfiles builder image
    if ! imageExists "build"; then
        docker/bin/docker_build.sh "build"
    fi
    dockerRun prod build docker/bin/build_staticfiles.sh
    echo "${GIT_COMMIT}" > static/revision.txt
    docker/bin/docker_build.sh "code"
fi

# build a tester image for non-demo deploys
if $TEST_MODE && ! imageExists "test"; then
    docker/bin/docker_build.sh "test"
fi

# include the data that the deployments need
if $DEMO_MODE && ! imageExists "demo"; then
    dockerRun demo code bin/sync-all.sh
    docker/bin/docker_build.sh "demo"
fi
if $PROD_MODE && ! imageExists "l10n"; then
    if [[ "$BRANCH_NAME" == "prod" ]]; then
        ENVFILE="prod";
    else
        ENVFILE="master";
    fi
    dockerRun $ENVFILE code "python manage.py l10n_update"
    docker/bin/docker_build.sh -c "locale" "l10n"
fi
