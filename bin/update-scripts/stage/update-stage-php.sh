#!/bin/sh

UPSTREAM=$(svn info http://svn.mozilla.org/projects/mozilla.com/tags/stage | grep Revision | cut -f2 -d' ')
cd /data/bedrock-stage/src/www.allizom.org

RUNNING=$(svnversion ./ | tr -d '[A-Z]')
UPDATED=0
if [ $RUNNING -ne $UPSTREAM ]; then
    svn -q up
    UPDATED=1
fi

cd org
RUNNING=$(svnversion ./ | tr -d '[A-Z]')
if [ $RUNNING -ne $UPSTREAM ]; then
    svn -q up
    UPDATED=1
fi

if [ $UPDATED = 1 ]; then
    /data/bedrock-stage/deploy www.allizom.org > /dev/null 2>&1
else
    # removed per bug 1087514
    # echo "Nothing to deploy."
    exit 0
fi
