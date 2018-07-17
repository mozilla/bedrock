#!/bin/bash

set -exo pipefail

source docker/bin/set_git_env_vars.sh

if [[ "$BRANCH_NAME" != "prod" ]]; then
    # nothing to do if not prod deployment
    exit 0
fi

CONTAINER_NAME="bedrock-${BRANCH_AND_COMMIT}"

rm -rf static
# have to rerun staticfiles without symlinks or we just copy broken symlinks
docker-compose run --name "$CONTAINER_NAME" release docker/bin/build_staticfiles.sh --nolink
docker cp "${CONTAINER_NAME}:/app/static" ./static
docker rm -f "$CONTAINER_NAME"

cd static
for BUCKET in stage prod; do
    # hashed filenames
    aws s3 sync \
        --exclude "*" \
        --include "*.????????????.*" \
        --acl public-read \
        --cache-control "max-age=315360000, public, immutable" \
        --profile bedrock-media \
        . "s3://bedrock-${BUCKET}-media/"
    # non-hashed filenames
    # may not need to include non-hashed files
    # TODO look into this if this is slow or makes the bucket too large
    aws s3 sync \
        --exclude "*.????????????.*" \
        --acl public-read \
        --cache-control "max-age=21600, public" \
        --profile bedrock-media \
        . "s3://bedrock-${BUCKET}-media/"
done

cd ..
rm -rf static
