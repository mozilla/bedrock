#!/bin/bash
# Needs DEIS_CONTROLLER URL, DEIS_USERNAME, DEIS_PASSWORD,
# DOCKER_REPOSITORY and DEIS_APPLICATION environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#

set -ex

deis login $DEIS_CONTROLLER  --username $DEIS_USERNAME --password $DEIS_PASSWORD
deis pull $DOCKER_REPOSITORY:$GIT_COMMIT -a $DEIS_APPLICATION
