#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys
from time import time

import boto3
from boto3.exceptions import Boto3Error
from db_utils import (
    DB_FILE,
    JSON_DATA_FILE,
    JSON_DATA_FILE_NAME,
    get_db_checksum,
    get_git_sha,
    get_prev_db_data,
    set_db_data,
)
from google.cloud import storage

# ROOT path of the project. A pathlib.Path object.
ROOT_PATH = Path(__file__).resolve().parents[1]
ROOT = str(ROOT_PATH)

# add bedrock to path
sys.path.append(ROOT)

# must import after adding bedrock to path
from bedrock.base.config_manager import config

CACHE = {}
BUCKET_NAME = os.getenv("AWS_DB_S3_BUCKET", "bedrock-db-dev")
REGION_NAME = os.getenv("AWS_DB_S3_REGION", "us-west-2")
UPLOAD_TO_GCS = config("UPLOAD_TO_GCS", parser=bool, default="false")


# Requires setting some environment variables:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# See boto3 docs for more info:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration
def s3_client():
    if "AWS_ACCESS_KEY_ID" not in os.environ:
        return None

    s3 = CACHE.get("s3_client")
    if not s3:
        s3 = boto3.client("s3", region_name=REGION_NAME)
        CACHE["s3_client"] = s3

    return s3


def gcs_client():
    gcs = CACHE.get("gcs_client")
    if not gcs:
        gcs = storage.Client()
        CACHE["gcs_client"] = gcs

    return gcs


def delete_s3_obj(filename):
    s3 = s3_client()
    s3.delete_object(Bucket=BUCKET_NAME, Key=filename)


def upload_db_data(db_data):
    s3 = s3_client()
    if not s3:
        return "ERROR: AWS credentials not configured"

    try:
        # upload the new db
        s3.upload_file(DB_FILE, BUCKET_NAME, db_data["file_name"], ExtraArgs={"ACL": "public-read"})
    except Boto3Error:
        return f"ERROR: Failed to upload the new database: {db_data}"

    try:
        # after successful file upload, upload json metadata
        s3.upload_file(JSON_DATA_FILE, BUCKET_NAME, JSON_DATA_FILE_NAME, ExtraArgs={"ACL": "public-read"})
    except Boto3Error:
        return f"ERROR: Failed to upload the new database info file: {db_data}"

    if UPLOAD_TO_GCS:
        gcs = gcs_client()
        bucket = gcs.bucket(BUCKET_NAME)

        # upload the database
        db_file = bucket.blob(db_data["file_name"])
        db_file.upload_from_filename(DB_FILE, predefined_acl="public-read")

        # upload the json metadata
        db_file_info = bucket.blob(JSON_DATA_FILE_NAME)
        db_file_info.upload_from_filename(JSON_DATA_FILE, predefined_acl="public-read")

    return 0


def get_db_file_name():
    git_sha = get_git_sha()
    checksum = get_db_checksum()
    return f"{git_sha[:10]}-{checksum[:10]}.db"


def get_db_data():
    return {
        "updated": time(),
        "checksum": get_db_checksum(),
        "git_sha": get_git_sha(),
        "file_name": get_db_file_name(),
    }


def main(args):
    force = "--force" in args
    prev_data = get_prev_db_data()
    new_data = get_db_data()
    if not force and prev_data and prev_data["checksum"] == new_data["checksum"]:
        print("No update necessary")
        return 0

    print("Attempting a db update")

    set_db_data(new_data)
    if "--no-upload" in args:
        return 0

    res = upload_db_data(new_data)
    # TODO decide if we should do this here or as a separate process
    # keeping some number of these around could be good for research
    # if res == 0 and prev_data:
    #    remove old db file
    #    delete_s3_obj(prev_data['file_name'])

    return res


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
