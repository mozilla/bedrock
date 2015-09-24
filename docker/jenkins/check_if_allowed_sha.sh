#!/bin/bash

# If commit is not a tag
if ! git describe --tags --exact-match $GIT_COMMIT > /dev/null 2>&1;
then
    # And if commit is not in master branch then exit.
    if ! git branch --contains $GIT_COMMIT 2> /dev/null | grep "* master" > /dev/null;
    then
        exit 1;
    fi;
fi;

# Commit is a tag or in master branch.
exit 0;
