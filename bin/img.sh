#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# are there images to optimize?
fileschanged=$(git diff --diff-filter=ACM --name-only HEAD | grep ".png\|.jpg\|.svg" | wc -l)
if [ $fileschanged == 0 ]; then
    echo "No images to optimize. Did you remember to stage them?"
    exit 1
fi

msgs=()

# ask to optimize with tinypng, we don't want to do this multiple times
read -p "Tinypng png and jpg images? " -n 1 -r
echo    # new line
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # is there a tinyPNG API key
    key="${HOME}/.tinypng"
    if ! [ -f "$key" ]; then
        echo "TinyPng API key not found."
        # let's save one, shall we?
        echo "What is your API key? (You can sign up for one here: https://tinypng.com/developers)"
        read apikey
        printf $apikey > ${HOME}/.tinypng
        echo "API key saved in $key"
    fi

    # tinypng png and jpg images
    git diff --diff-filter=ACM --name-only HEAD | grep ".png\|.jpg" | xargs ./node_modules/tinypng-cli/tinypng-cli.js
fi

# svgo svg images
echo "Optimizing SVGs..."
git diff --diff-filter=ACM --name-only HEAD | grep ".svg" | xargs ./node_modules/svgo/bin/svgo --disable=removeViewBox

# check SVGs have viewbox
echo "Checking for viewboxes..."
svgs=$(git diff --diff-filter=ACM --name-only HEAD | grep ".svg")
for svg in $svgs; do
    if ! grep -qi viewbox "$svg"; then
        msgs+=("✘ $svg is missing viewbox")
    fi
done

# check -high-res have corresponding low res
echo "Checking high-res images have a matching low-res..."
highresimages=$(git diff --diff-filter=ACM --name-only HEAD | grep "\-high\-res")
for highresimage in $highresimages; do
    lowresimage=${highresimage/-high-res/}
    if ! [ -f "$lowresimage" ]; then
        msgs+=("✘ $lowresimage not found")
    fi
done

if [ ${#msgs[@]} -eq 0 ]; then
    echo "... done. Everything looks good!"
    exit 0
else
    echo "... hmmm something isn't right."
    for i in "${msgs[@]}"; do
        echo $i
    done
    exit 1
fi
