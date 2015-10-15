#!/bin/bash
# Needs DEIS_CONTROLLER URL, DEIS_USERNAME, DEIS_PASSWORD,
# DOCKER_REPOSITORY, DEIS_APPLICATION, NEWRELIC_API_KEY and
# NEWRELIC_APP_NAME environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#

set -ex

deis login $DEIS_CONTROLLER  --username $DEIS_USERNAME --password $DEIS_PASSWORD
deis pull $DOCKER_REPOSITORY:$GIT_COMMIT -a $DEIS_APPLICATION
curl -H "x-api-key:$NEWRELIC_API_KEY" \
     -d "deployment[app_name]=$NEWRELIC_APP_NAME" \
     -d "deployment[revision]=$GIT_COMMIT" \
     -d "deployment[user]=EE Jenkins" \
     https://api.newrelic.com/deployments.xml
