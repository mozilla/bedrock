#!/bin/bash
# Needs DEIS_PROFILE, DOCKER_REPOSITORY, DEIS_APPLICATION, NEWRELIC_API_KEY and
# NEWRELIC_APP_NAME environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#

set -ex

deis pull "$DOCKER_REPOSITORY:$GIT_COMMIT" -a $DEIS_APPLICATION
if [[ -n "$NEWRELIC_API_KEY" ]]; then
    curl -H "x-api-key:$NEWRELIC_API_KEY" \
         -d "deployment[app_name]=$NEWRELIC_APP_NAME" \
         -d "deployment[revision]=$GIT_COMMIT" \
         -d "deployment[user]=EE Jenkins" \
         https://api.newrelic.com/deployments.xml
fi
