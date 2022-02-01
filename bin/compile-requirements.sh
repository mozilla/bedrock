#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

export CUSTOM_COMPILE_COMMAND="make compile-requirements"

# We need this installed, but we don't want it to live in the main requirements
# We will need to periodically review this pinning
pip install pip-tools==6.4.0  # needs at least this version to build
pip install pip-compile-multi

pip-compile-multi \
    --generate-hashes prod \
    --generate-hashes dev \
    --generate-hashes docs \
    --header=/app/bin/pip-compile-multi-header-message.txt
