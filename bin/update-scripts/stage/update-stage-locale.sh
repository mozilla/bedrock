#!/bin/bash

UPSTREAM=$(svn info https://svn.mozilla.org/projects/mozilla.com/trunk/locales | grep Revision | cut -f2 -d' ')
cd /data/bedrock-stage/src/www.allizom.org-django/bedrock

pushd locale > /dev/null
RUNNING=$(svnversion ./ | tr -d '[A-Z]')
UPDATED=0
if [ "$RUNNING" != "$UPSTREAM" ]; then
    svn -q up
    UPDATED=1
fi
popd > /dev/null

if [ $UPDATED -eq 1 ]; then
    /data/bedrock-stage/deploy -q www.allizom.org-django/bedrock/locale
else
#    echo "Nothing to deploy."
    exit 0
fi
