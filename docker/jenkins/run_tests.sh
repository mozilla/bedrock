#!/bin/bash
#
# Runs unit_tests
#
set -ex

ENV_FILE=`mktemp`
cat << EOF > $ENV_FILE
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,
SECRET_KEY=39114b6a-2858-4caf-8878-482a24ee9542
ADMINS=["thedude@example.com"]
EOF

docker run --env-file $ENV_FILE ${DOCKER_REPOSITORY}:${GIT_COMMIT:-$(git rev-parse HEAD)} ./manage.py test
