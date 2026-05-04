#! /bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

# Set the command used in the reminder comment at the top of the file
export UV_CUSTOM_COMPILE_COMMAND="$ make compile-requirements"

# Ensure we've got the latest `uv`
pip install -U uv

# Drop the compiled reqs files, to help us pick up automatic subdep updates, too
rm -f requirements/*.txt

# --exclude-newer='7 days' avoids packages uploaded in the last 7 days
# reducing supply-chain risk. To apply urgent security patch (e.g. Django):
# update version pin in requirements/prod.in, then run:
# uv pip compile --upgrade-package Django --exclude-newer='7 days' --generate-hashes --no-strip-extras --python-version 3.13 requirements/prod.in -o requirements/prod.txt
uv pip compile --exclude-newer='7 days' --generate-hashes --no-strip-extras --python-version 3.13 requirements/prod.in -o requirements/prod.txt
uv pip compile --exclude-newer='7 days' --generate-hashes --no-strip-extras --python-version 3.13 requirements/dev.in -o requirements/dev.txt
uv pip compile --exclude-newer='7 days' --generate-hashes --no-strip-extras --python-version 3.13 requirements/docs.in -o requirements/docs.txt
