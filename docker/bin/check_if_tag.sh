#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
