#!/bin/sh

UPSTREAM=$(svn info https://svn.mozilla.org/projects/mozilla.org/trunk | grep Revision | cut -f2 -d' ')
cd /data/bedrock-dev/src/www-dev.allizom.org

RUNNING=$(svnversion ./ | tr -d '[A-Z]')
UPDATED=0
if [ "$RUNNING" != "$UPSTREAM" ]; then
    svn cleanup
    svn -q up
    UPDATED=1
fi

cd org
RUNNING=$(svnversion ./ | tr -d '[A-Z]')
if [ "$RUNNING" != "$UPSTREAM" ]; then
    svn cleanup
    svn -q up
    UPDATED=1
fi

if [ $UPDATED -eq 1 ]; then
    /data/bedrock-dev/deploy www-dev.allizom.org > /dev/null 2>&1
else
    # removing per bug 1087514
    #    echo "Nothing to deploy."
    exit 0
fi
