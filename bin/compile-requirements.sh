#! /bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

# Set the command used in the reminder comment at the top of the file
export CUSTOM_COMPILE_COMMAND="$ make compile-requirements"

# We need this installed, but we don't want it to live in the main requirements
# We will need to periodically review this pinning

pip install -U pip==22.0.3
pip install pip-tools==6.5.0

pip-compile --generate-hashes -r requirements/inputs/prod.in -o requirements/prod.txt
pip-compile --generate-hashes -r requirements/inputs/dev.in -o requirements/dev.txt
pip-compile --generate-hashes -r requirements/inputs/docs.in -o requirements/docs.txt
