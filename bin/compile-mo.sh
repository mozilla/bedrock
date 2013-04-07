#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


TARGET=$1
LOCKFILE="/tmp/compile-mo-${2}.lock"

function usage() {
    echo "syntax:"
    echo "  compile-mo.sh locale-dir/ [unique]"
    echo "unique is an optional string that will be used as the name of the lockfile"
    exit 1
}

# check if file and dir are there
if [[ ($# -gt 2) || (! -d "$TARGET") ]]; then usage; fi

# check if the lockfile exists
if [ -e $LOCKFILE ]; then
    echo "$LOCKFILE present, exiting"
    exit 99
fi

touch $LOCKFILE
for lang in `find $TARGET -type f -name "*.po"`; do
    dir=`dirname $lang`
    stem=`basename $lang .po`
    msgfmt -o ${dir}/${stem}.mo $lang
done
rm $LOCKFILE
