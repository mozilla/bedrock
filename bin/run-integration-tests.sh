#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

set -xe

# Defaults
: ${PYTEST_PROCESSES:="1"}
: ${BASE_URL:="https://www-dev.allizom.org"}
: ${SELENIUM_HOST:="localhost"}
: ${SELENIUM_PORT:="4444"}
: ${BROWSER_NAME:="firefox"}
: ${TESTS_PATH:="tests"}
: ${RESULTS_PATH:="${TESTS_PATH}/results"}

# Common arguments
CMD="py.test"
CMD="${CMD} -r a"
CMD="${CMD} --verbose"
CMD="${CMD} -n ${PYTEST_PROCESSES}"
CMD="${CMD} --base-url ${BASE_URL}"
# rerun a flaky test once
# DO NOT INCREASE THIS
CMD="${CMD} --reruns 1"
CMD="${CMD} --html ${RESULTS_PATH}/index.html"
CMD="${CMD} --junitxml ${RESULTS_PATH}/junit.xml"
if [ -n "${DRIVER}" ]; then CMD="${CMD} --driver ${DRIVER}"; fi

# Remote arguments
if [ "${DRIVER}" = "Remote" ]; then
  CMD="${CMD} --host ${SELENIUM_HOST}"
  CMD="${CMD} --port ${SELENIUM_PORT}"
  CMD="${CMD} --capability browserName \"${BROWSER_NAME}\""
  if [ -n "${BROWSER_VERSION}" ]; then CMD="${CMD} --capability version \"${BROWSER_VERSION}\""; fi
  if [ -n "${PLATFORM}" ]; then CMD="${CMD} --capability platform \"${PLATFORM}\""; fi
fi

# Sauce Labs arguments
if [ "${DRIVER}" = "SauceLabs" ]; then
  CMD="${CMD} --capability browserName \"${BROWSER_NAME}\""
  if [ -n "${BROWSER_VERSION}" ]; then CMD="${CMD} --capability version \"${BROWSER_VERSION}\""; fi
  if [ -n "${PLATFORM}" ]; then CMD="${CMD} --capability platform \"${PLATFORM}\""; fi
  if [ -n "${SELENIUM_VERSION}" ]; then CMD="${CMD} --capability selenium-version \"${SELENIUM_VERSION}\""; fi
  if [ -n "${BUILD_TAG}" ]; then CMD="${CMD} --capability build \"${BUILD_TAG}\""; fi
  if [ -n "${SCREEN_RESOLUTION}" ]; then CMD="${CMD} --capability screenResolution \"${SCREEN_RESOLUTION}\""; fi
  if [ -n "${PRIVACY}" ]; then CMD="${CMD} --capability public \"${PRIVACY}\""; fi
fi

if [ -n "${MARK_EXPRESSION}" ]; then CMD="${CMD} -m \"${MARK_EXPRESSION}\""; fi

CMD="${CMD} ${TESTS_PATH}"
eval ${CMD}
