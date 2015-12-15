#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

set -xe

CMD="linkchecker"
CMD="${CMD} -F html/utf8//results/linkchecker-out.html"
if [ -n "${THREADS}" ]; then CMD="${CMD} -t ${THREADS}"; fi
if [ -n "${RECURSION_LEVEL}" ]; then CMD="${CMD} -r ${RECURSION_LEVEL}"; fi
if [ "${VERBOSE}" = "true" ]; then CMD="${CMD} -v"; fi
if [ "${CHECK_EXTERNAL}" = "true" ]; then CMD="${CMD} --check-extern"; fi

CMD="${CMD} ${URLS}"
eval ${CMD}
