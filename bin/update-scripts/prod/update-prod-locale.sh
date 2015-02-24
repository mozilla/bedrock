#!/bin/bash

UPSTREAM=$(svn info https://svn.mozilla.org/projects/mozilla.com/trunk/locales | grep Revision | cut -f2 -d' ')
cd /data/bedrock/src/www.mozilla.org-django/bedrock

pushd locale > /dev/null
RUNNING=$(svnversion ./ | tr -d '[A-Z]')
if [ "$RUNNING" != "$UPSTREAM" ]; then
    svn -q up
    echo -e "finished at $(date)" > /data/bedrock/src/www.mozilla.org-django/bedrock/media/locale_finished.txt
    exit 0
fi
popd > /dev/null

exit 1
