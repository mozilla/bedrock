#!/bin/sh

URL=${URL:-"https://ci.us-west.moz.works/job/bedrock_base_image/buildWithParameters"}
TAG=$1

if [ -z "$1" ]
  then
      echo "Usage: $0 <tag>"
      exit 0;
fi

curl -X POST "$URL?delay=0&token=$WEBHOOK_SECRET&TAG=$TAG"
