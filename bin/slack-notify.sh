#!/bin/bash
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -eo pipefail

# Required environment variables if using --stage:
# BRANCH_NAME, BUILD_NUMBER

# defaults and constants
CHANNEL="www-notify"
CHANNEL_FAILURE="meao-alerts"
BLUE_BUILD_URL="https://ci.vpn1.moz.works/blue/organizations/jenkins/bedrock_multibranch_pipeline"
BLUE_BUILD_URL="${BLUE_BUILD_URL}/detail/${BRANCH_NAME/\//%2f}/${BUILD_NUMBER}/pipeline"

# parse cli args
while [[ $# -gt 1 ]]; do
    key="$1"
    case $key in
        --stage)
            STAGE="$2"
            shift # past argument
            ;;
        --status)
            STATUS="$2"
            shift # past argument
            ;;
        -m|--message)
            MESSAGE="$2"
            shift # past argument
            ;;
    esac
    shift # past argument or value
done

if [[ -n "$STATUS" ]]; then
    STATUS=$(echo "$STATUS" | tr '[:lower:]' '[:upper:]')
    case "$STATUS" in
      'SUCCESS')
        STATUS_PREFIX=":tada:"
        ;;
      'SHIPPED')
        STATUS_PREFIX=":ship:"
        ;;
      'WARNING')
        STATUS_PREFIX=":warning:"
        ;;
      'FAILURE')
        STATUS_PREFIX=":rotating_light:"
        ;;
      *)
        STATUS_PREFIX=":sparkles:"
        ;;
    esac
    STATUS="${STATUS_PREFIX} *${STATUS}*: "
fi

# add project name
STATUS="*bedrock*: ${STATUS}"

if [[ -n "$STAGE" ]]; then
    MESSAGE="${STATUS}${STAGE}:"
    MESSAGE="$MESSAGE Branch *${BRANCH_NAME}* <${BLUE_BUILD_URL}|build #${BUILD_NUMBER}>"
elif [[ -n "$MESSAGE" ]]; then
    MESSAGE="${STATUS}${MESSAGE}"
else
    echo "Missing required arguments"
    echo
    echo "Usage: slack-notify.sh [--stage STAGE]|[-m MESSAGE]"
    echo "Optional args: --status"
    exit 1
fi

slack-cli -d "${CHANNEL}" "${MESSAGE}" || true

if [[ "${STATUS}-${BRANCH_NAME}" == "FAILURE-prod" ]]; then
    slack-cli -d "${CHANNEL_FAILURE}" "${MESSAGE}" || true
fi
