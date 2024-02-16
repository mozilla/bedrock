#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

set -exo pipefail

source docker/bin/set_git_env_vars.sh

if [[ "$BRANCH_NAME" == "prod" ]]; then
    BUCKETS=(prod)
elif [[ "$BRANCH_NAME" == "stage" ]]; then
    BUCKETS=(stage)
elif [[ "$BRANCH_NAME" == "main" ]]; then
    BUCKETS=(dev)
else
    # nothing to do if not prod deployment
    exit 0
fi

TMP_DIR="s3-static"
TMP_DIR_HASHED="s3-static-hashed"
CONTAINER_NAME="bedrock-${GIT_COMMIT}"

rm -rf "${TMP_DIR}"
rm -rf "${TMP_DIR_HASHED}"

# .env file must exist for docker-compose
touch .env

# have to rerun staticfiles without symlinks or we just copy broken symlinks
docker rm -f "$CONTAINER_NAME" || true
docker-compose run --name "$CONTAINER_NAME" release docker/bin/build_staticfiles.sh --nolink
docker cp "${CONTAINER_NAME}:/app/static" "${TMP_DIR}"
docker rm -f "$CONTAINER_NAME"

# separate the hashed files into another directory
bin/move_hashed_staticfiles.py "${TMP_DIR}" "${TMP_DIR_HASHED}"

for BUCKET in "${BUCKETS[@]}"; do
    # hashed filenames
    aws s3 sync \
        --acl public-read \
        --cache-control "max-age=315360000, public, immutable" \
        "./${TMP_DIR_HASHED}" "s3://bedrock-${BUCKET}-media/media/"
    # non-hashed filenames
    # may not need to include non-hashed files
    # TODO look into this if this is slow or makes the bucket too large
    aws s3 sync \
        --acl public-read \
        --cache-control "max-age=21600, public" \
        "./${TMP_DIR}" "s3://bedrock-${BUCKET}-media/media/"
done

rm -rf "${TMP_DIR}"
rm -rf "${TMP_DIR_HASHED}"
