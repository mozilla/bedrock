#!/bin/bash

cd /data/bedrock-stage/src/www.allizom.org-django/bedrock

pushd locale > /dev/null
CUR_REV=$(git rev-parse HEAD)
git pull --ff-only origin master > /dev/null
NEW_REV=$(git rev-parse HEAD)
popd > /dev/null

if [ "$NEW_REV" != "$CUR_REV" ]; then
    echo "Deploying new locales: ${NEW_REV:0:10}"
    /data/bedrock-stage/deploy -q www.allizom.org-django/bedrock/locale
fi
