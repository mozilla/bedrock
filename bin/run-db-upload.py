#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sys
from pathlib import Path
from time import time

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
from bedrock.base.config_manager import config  # noqa

CACHE = {}
BUCKET_NAME = config("AWS_DB_S3_BUCKET", default="bedrock-db-dev")


def gcs_client():
    gcs = CACHE.get("gcs_client")
    if not gcs:
        gcs = storage.Client()
        CACHE["gcs_client"] = gcs

    return gcs


def upload_db_data(db_data):
    gcs = gcs_client()
    bucket = gcs.bucket(BUCKET_NAME)

    # upload the database
    db_file = bucket.blob(db_data["file_name"])
    db_file.upload_from_filename(DB_FILE)

    # upload the json metadata
    db_file_info = bucket.blob(JSON_DATA_FILE_NAME)
    db_file_info.upload_from_filename(JSON_DATA_FILE)

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

    return upload_db_data(new_data)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
