#!/usr/bin/env python
import json
import os

STATIC = './static/staticfiles.json'

with open(STATIC) as static_fp:
    static_files = json.load(static_fp)

for orig, hashed in list(static_files['paths'].items()):
    if '?' in orig:
        continue

    if orig.endswith('.css'):
        # contents of hashed css files have been modified to referenced
        # other hashed files (images and whatnot). We want to keep that.
        continue

    hashed_path = os.path.join('./static', hashed)
    orig_filename = os.path.split(orig)[1]

    # no exception handling b/c we want to abort on OS errors here
    os.unlink(hashed_path)
    os.symlink(orig_filename, hashed_path)
