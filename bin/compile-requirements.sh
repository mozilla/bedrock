#! /bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

# Set the command used in the reminder comment at the top of the file
export UV_CUSTOM_COMPILE_COMMAND="$ make compile-requirements"

# We need this installed, but we don't want it to live in the main requirements
pip install -U uv

# Drop the compiled reqs files, to help us pick up automatic subdep updates, too
rm -f requirements/*.txt

uv pip compile --generate-hashes --no-strip-extras requirements/prod.in -o requirements/prod.txt
uv pip compile --generate-hashes --no-strip-extras requirements/dev.in -o requirements/dev.txt
uv pip compile --generate-hashes --no-strip-extras requirements/docs.in -o requirements/docs.txt
