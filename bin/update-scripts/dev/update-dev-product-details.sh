#!/bin/bash

DEPLOY_SCRIPT=/data/bedrock-dev/deploy
WORKING_DIR=/data/bedrock-dev/src/www-dev.allizom.org-django/bedrock
SITE_NAME=www-dev.allizom.org
PYTHON=../venv/bin/python
PD_PATH=lib/product_details_json

cd $WORKING_DIR
$PYTHON manage.py update_product_details
$DEPLOY_SCRIPT -q "${SITE_NAME}-django/bedrock/$PD_PATH"
exit 0
