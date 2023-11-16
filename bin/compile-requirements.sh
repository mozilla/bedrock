#! /bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

# Set the command used in the reminder comment at the top of the file
export CUSTOM_COMPILE_COMMAND="$ make compile-requirements"

# We need this installed, but we don't want it to live in the main requirements
# We will need to periodically review this pinning

pip install -U pip==23.1.2
pip install pip-tools==6.13.0

pip-compile --generate-hashes -r requirements/prod.in --resolver=backtracking --rebuild
pip-compile --generate-hashes -r requirements/dev.in --resolver=backtracking --rebuild
