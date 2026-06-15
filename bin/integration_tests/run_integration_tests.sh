#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -xe

# Defaults
: ${PYTEST_PROCESSES:="1"}
: ${BASE_URL:="https://www-dev.allizom.org"}
: ${BOUNCER_URL:="https://download.mozilla.org/"}
: ${TESTS_PATH:="tests"}
: ${RESULTS_PATH:="${TESTS_PATH}/results"}
: ${RERUNS_ALLOWED:="2"}
: ${RERUNS_DELAY_SECS:="1"}

CMD="pytest"
CMD="${CMD} -r a"
CMD="${CMD} --verbose"
CMD="${CMD} --workers ${PYTEST_PROCESSES}"
CMD="${CMD} --base-url ${BASE_URL}"
CMD="${CMD} --reruns ${RERUNS_ALLOWED}"
CMD="${CMD} --reruns-delay ${RERUNS_DELAY_SECS}"
CMD="${CMD} --html ${RESULTS_PATH}/index.html"
CMD="${CMD} --junitxml ${RESULTS_PATH}/junit.xml"

if [ -n "${MARK_EXPRESSION}" ]; then CMD="${CMD} -m \"${MARK_EXPRESSION}\""; fi

CMD="${CMD} ${TESTS_PATH}"
eval ${CMD}
