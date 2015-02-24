#!/bin/sh

UPSTREAM=$(svn info http://svn.mozilla.org/projects/mozilla.com/tags/production | grep Revision | cut -f2 -d' ')
cd /data/bedrock/src/www.mozilla.org

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
    /data/bedrock/deploy www.mozilla.org > /dev/null 2>&1
else
#    echo "Nothing to deploy."
    exit 0
fi
