#!/bin/bash
set -eo pipefail

# Required environment variables if using --stage and --status:
# BRANCH_NAME, BUILD_NUMBER, BUILD_URL

# defaults and constants
BUILD_NUMBER="${BUILD_NUMBER:-0}"
NICK="bedrock-deployer-$BUILD_NUMBER"
CHANNEL="#www"
SERVER="irc.mozilla.org:6697"
# colors and styles: values from the following links
# http://www.mirc.com/colors.html
# http://stackoverflow.com/a/13382032
RED=$'\x034'
YELLOW=$'\x038'
GREEN=$'\x039'
BLUE=$'\x0311'
BOLD=$'\x02'
NORMAL=$'\x0F'

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
        --demo_url)
            DEMO_URL="$2"
            shift # past argument
            ;;
        -m|--message)
            MESSAGE="$2"
            shift # past argument
            ;;
        --irc_nick)
            NICK="$2-$BUILD_NUMBER"
            shift # past argument
            ;;
        --irc_server)
            SERVER="$2"
            shift # past argument
            ;;
        --irc_channel)
            CHANNEL="$2"
            shift # past argument
            ;;
    esac
    shift # past argument or value
done

if [[ -z "$MESSAGE" ]]; then
    if [[ -n "$STATUS" ]]; then
        STATUS=$(echo "$STATUS" | tr '[:lower:]' '[:upper:]')
        case "$STATUS" in
          'SUCCESS')
            STATUS_COLOR="${BOLD}${GREEN}"
            ;;
          'WARNING')
            STATUS_COLOR="${BOLD}${YELLOW}"
            ;;
          'FAILURE')
            STATUS_COLOR="${BOLD}${RED}"
            ;;
          *)
            STATUS_COLOR="$BLUE"
            ;;
        esac
        MESSAGE="${STATUS_COLOR}${STATUS}${NORMAL}: ${STAGE}:"
        MESSAGE="$MESSAGE Branch ${BOLD}${BRANCH_NAME}${NORMAL} build #${BUILD_NUMBER}: ${BUILD_URL}"
    elif [[ -n "$DEMO_URL" ]]; then
        MESSAGE="${BOLD}${GREEN}SUCCESS${NORMAL}: Demo deployed: ${DEMO_URL}"
    else
        echo "Missing required arguments"
        echo
        echo "Usage: irc-notify.sh [--stage STAGE --status STATUS] [--demo_url DEMO_URL]"
        echo "Optional args: --irc_nick, --irc_server, --irc_channel"
        exit 1
    fi
fi

(
  echo "NICK ${NICK}"
  echo "USER ${NICK} 8 * : ${NICK}"
  sleep 5
  echo "JOIN ${CHANNEL}"
  echo "NOTICE ${CHANNEL} :${MESSAGE}"
  echo "QUIT"
) | openssl s_client -connect "$SERVER" > /dev/null 2>&1
