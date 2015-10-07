#!/usr/bin/env python
import json
import os

STATIC = './static/staticfiles.json'

with open(STATIC) as static_fp:
    static_files = json.load(static_fp)

for orig, hashed in static_files['paths'].items():
    if '?' in orig:
        continue
    hashed_path = os.path.join('./static', hashed)
    orig_filename = os.path.split(orig)[1]

    # no exception handling b/c we want to abort on OS errors here
    os.unlink(hashed_path)
    os.symlink(orig_filename, hashed_path)
