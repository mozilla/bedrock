#!/bin/bash

TAG=$(git describe --tags --exact-match $GIT_COMMIT 2> /dev/null)
if [[ -n "$TAG" ]]; then
    if [[ "$TAG" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}(\.[0-9])?$ ]]; then
        echo "Build tagged as $TAG"
        exit 0
    else
        echo "Build tagged but in the wrong format: $TAG"
        exit 1
    fi
else
    echo "Build not tagged"
    exit 1
fi
