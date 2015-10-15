#!/bin/bash -ex
# Needs DEIS_CONTROLLER URL, DEIS_USERNAME, DEIS_PASSWORD,
# DEIS_PROFILE, and DEIS_APPLICATION environment variables.
#
# To set them go to Job -> Configure -> Build Environment -> Inject
# passwords and Inject env variables
#

deis login $DEIS_CONTROLLER --username=$DEIS_USERNAME --password=$DEIS_PASSWORD
deis run -a $DEIS_APPLICATION -- './manage.py runscript clock'
