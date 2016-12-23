#!/bin/bash

# Used to trigger downstream Jenkins jobs
TRIGGER_FILE=".commit_is_tag"
rm -rf $TRIGGER_FILE

TAG=$(git describe --tags --exact-match $GIT_COMMIT 2> /dev/null)
if [[ -n "$TAG" ]] && [[ "$TAG" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}(\.[0-9])?$ ]]; then
    touch $TRIGGER_FILE
fi;
