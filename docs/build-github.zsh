#!/bin/zsh
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Should be run from the docs directory: (cd docs && ./build-github.zsh)

REPO=$(git config remote.origin.url)
HERE=$(dirname $0)
GH=$HERE/_gh-pages


# Checkout the gh-pages branch, if necessary.
if [[ ! -d $GH ]]; then
    git clone $REPO $GH
    pushd $GH
    git checkout -b gh-pages origin/gh-pages
    popd
fi

# Update and clean out the _gh-pages target dir.
pushd $GH
git pull && rm -rf *
popd

# Make a clean build.
pushd $HERE
make clean dirhtml

# Move the fresh build over.
cp -r _build/dirhtml/* $GH
pushd $GH

# Commit.
git add .
git commit -am "gh-pages build on $(date)"
git push origin gh-pages

popd
popd
