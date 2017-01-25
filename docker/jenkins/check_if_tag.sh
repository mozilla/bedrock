#!/bin/bash

TAG=$(git describe --tags --exact-match $GIT_COMMIT 2> /dev/null)
[[ -n "$TAG" ]] && [[ "$TAG" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}(\.[0-9])?$ ]]
