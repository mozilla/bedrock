#!/bin/bash
# Needs DEIS_CONTROLLER URL, DEIS_USERNAME, DEIS_PASSWORD,
# DOCKER_REPOSITORY and DEIS_APPLICATION environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#

set -ex

# Create a temporary virtualenv to install deis client
TDIR=`mktemp -d`
virtualenv $TDIR
. $TDIR/bin/activate
pip install deis==1.8.0


deis login $DEIS_CONTROLLER  --username $DEIS_USERNAME --password $DEIS_PASSWORD
deis pull $DOCKER_REPOSITORY:`git rev-parse HEAD` -a $DEIS_APPLICATION
