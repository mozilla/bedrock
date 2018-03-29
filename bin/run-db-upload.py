#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys
from time import time

import boto3
from boto3.exceptions import Boto3Error

from db_s3_utils import (
    get_db_checksum,
    get_git_sha,
    get_prev_db_data,
    set_db_data,
    JSON_DATA_FILE,
    DB_FILE,
)


CACHE = {}
BUCKET_NAME = os.getenv('AWS_DB_S3_BUCKET', 'bedrock-db-dev')
REGION_NAME = os.getenv('AWS_DB_S3_REGION', 'us-west-2')


# Requires setting some environment variables:
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# See boto3 docs for more info:
# http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variable-configuration
def s3_client():
    if 'AWS_ACCESS_KEY_ID' not in os.environ:
        return None

    s3 = CACHE.get('s3_client')
    if not s3:
        s3 = boto3.client('s3', region_name=REGION_NAME)
        CACHE['s3_client'] = s3

    return s3


def delete_s3_obj(filename):
    s3 = s3_client()
    s3.delete_object(Bucket=BUCKET_NAME, Key=filename)


def upload_db_data(db_data):
    s3 = s3_client()
    if not s3:
        return 'ERROR: AWS credentials not configured'

    try:
        # upload the new db
        s3.upload_file(DB_FILE, BUCKET_NAME, db_data['file_name'],
                       ExtraArgs={'ACL': 'public-read'})
    except Boto3Error:
        return 'ERROR: Failed to upload the new database: %s' % db_data

    try:
        # after successful file upload, upload json metadata
        s3.upload_file(JSON_DATA_FILE, BUCKET_NAME, JSON_DATA_FILE,
                       ExtraArgs={'ACL': 'public-read'})
    except Boto3Error:
        return 'ERROR: Failed to upload the new database info file: %s' % db_data

    return 0


def get_db_file_name():
    git_sha = get_git_sha()
    checksum = get_db_checksum()
    return '{}-{}.db'.format(git_sha[:10], checksum[:10])


def get_db_data():
    return {
        'updated': time(),
        'checksum': get_db_checksum(),
        'git_sha': get_git_sha(),
        'file_name': get_db_file_name(),
    }


def main(args):
    force = '--force' in args
    prev_data = get_prev_db_data()
    new_data = get_db_data()
    if not force and prev_data and prev_data['checksum'] == new_data['checksum']:
        print('No update necessary')
        return 0

    set_db_data(new_data)
    if '--no-upload' in args:
        return 0

    res = upload_db_data(new_data)
    # TODO decide if we should do this here or as a separate process
    # keeping some number of these around could be good for research
    # if res == 0 and prev_data:
    #    remove old db file
    #    delete_s3_obj(prev_data['file_name'])

    return res


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
