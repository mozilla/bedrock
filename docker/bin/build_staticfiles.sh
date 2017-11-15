#!/bin/bash

set -euxo pipefail

if [[ "$BRANCH_NAME" == "prod" ]]; then
    ENV_FILE=prod
else
    ENV_FILE=master
fi

honcho run --env "docker/envfiles/${ENV_FILE}.env" python manage.py collectstatic --link --noinput -v 0
python docker/bin/softlinkstatic.py
