#!/bin/bash

BIN_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $BIN_DIR/set_git_env_vars.sh

if [[ -n "$GIT_TAG" ]]; then
    if [[ "$GIT_TAG_DATE_BASED" == true ]]; then
        echo "Build tagged as $GIT_TAG"
        exit 0
    else
        echo "Build tagged but in the wrong format: $GIT_TAG"
        exit 1
    fi
else
    echo "Build not tagged"
    exit 1
fi
