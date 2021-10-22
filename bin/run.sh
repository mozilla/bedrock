#!/bin/bash -xe

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

RUN_SUPERVISOR=$(echo "${RUN_SUPERVISOR:-true}" | tr '[:upper:]' '[:lower:]')

if [[ "$RUN_SUPERVISOR" == "true" ]]; then
  exec bin/run-supervisor.sh
else
  exec bin/run-prod.sh
fi
