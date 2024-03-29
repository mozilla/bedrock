#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os

STATIC = "./static/staticfiles.json"

with open(STATIC) as static_fp:
    static_files = json.load(static_fp)

for orig, hashed in static_files["paths"].items():
    if "?" in orig:
        continue

    if orig.endswith(".css"):
        # contents of hashed css files have been modified to referenced
        # other hashed files (images and whatnot). We want to keep that.
        continue

    hashed_path = os.path.join("./static", hashed)
    orig_filename = os.path.split(orig)[1]

    # no exception handling b/c we want to abort on OS errors here
    os.unlink(hashed_path)
    os.symlink(orig_filename, hashed_path)
