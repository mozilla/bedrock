#!/bin/bash

set -exo pipefail

source docker/bin/set_git_env_vars.sh

if [[ "$BRANCH_NAME" == "prod" ]]; then
    BUCKETS=(stage prod)
elif [[ "$BRANCH_NAME" == "master" ]]; then
    BUCKETS=(dev)
else
    # nothing to do if not prod deployment
    exit 0
fi

TMP_DIR="s3-static"
TMP_DIR_HASHED="s3-static-hashed"
CONTAINER_NAME="bedrock-${BRANCH_AND_COMMIT}"

rm -rf "${TMP_DIR}"
rm -rf "${TMP_DIR_HASHED}"

# have to rerun staticfiles without symlinks or we just copy broken symlinks
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
        --profile bedrock-media \
        "./${TMP_DIR_HASHED}" "s3://bedrock-${BUCKET}-media/media/"
    # non-hashed filenames
    # may not need to include non-hashed files
    # TODO look into this if this is slow or makes the bucket too large
    aws s3 sync \
        --acl public-read \
        --cache-control "max-age=21600, public" \
        --profile bedrock-media \
        "./${TMP_DIR}" "s3://bedrock-${BUCKET}-media/media/"
done

rm -rf "${TMP_DIR}"
rm -rf "${TMP_DIR_HASHED}"
