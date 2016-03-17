#!/bin/bash

set -e

curl -d "delay=0" -d "token=$JENKINS_WEBHOOK_TOKEN" \
  https://ci.us-west.moz.works/job/bedrock_base_image/buildWithParameters
