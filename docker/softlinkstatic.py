#!/usr/bin/env python
import json
import os

STATIC = './static/staticfiles.json'

with open(STATIC) as static_fp:
    static_files = json.load(static_fp)

for orig, hashed in static_files['paths'].items():
    if '?' in orig:
        continue
    orig_path = os.path.join('./static', orig)
    hashed_filename = os.path.split(hashed)[1]
    # no exception handling b/c we want to abort on OS errors here
    os.unlink(orig_path)
    os.symlink(hashed_filename, orig_path)
