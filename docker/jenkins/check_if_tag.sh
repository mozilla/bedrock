#!/bin/bash

# Used to trigger downstream Jenkins jobs
TRIGGER_FILE=.commit_is_tag
rm -rf $TRIGGER_FILE

if git describe --tags --exact-match $GIT_COMMIT 2> /dev/null;
then
    touch $TRIGGER_FILE
fi;
