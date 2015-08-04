#!/usr/bin/env python
import json
import os

STATIC = './static/staticfiles.json'

with open(STATIC) as static_fp:
    static_files = json.load(static_fp)

for path in static_files['paths']:
    full_path = os.path.join('./static', path)

    try:
        os.unlink(full_path)
    except OSError:
        pass
