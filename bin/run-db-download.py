#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals

import os
import sys

import requests

from db_s3_utils import (
    get_db_checksum,
    get_git_sha,
    get_prev_db_data,
    set_db_data,
    JSON_DATA_FILE,
    DB_FILE,
)


BUCKET_NAME = os.getenv('AWS_DB_S3_BUCKET', 'bedrock-db-dev')
REGION_NAME = os.getenv('AWS_DB_REGION', 'us-west-2')
S3_BASE_URL = 'https://s3-{}.amazonaws.com/{}'.format(
    REGION_NAME,
    BUCKET_NAME,
)


def get_file_url(filename):
    return '/'.join([S3_BASE_URL, filename])


def download_db_info():
    try:
        resp = requests.get(get_file_url(JSON_DATA_FILE))
        resp.raise_for_status()
    except requests.RequestException:
        return None

    try:
        return resp.json()
    except ValueError:
        # not JSON
        return None


def download_db_file(filename):
    resp = requests.get(get_file_url(filename), stream=True)
    with open(filename, 'wb') as fp:
        for chunk in resp.iter_content(chunk_size=128):
            fp.write(chunk)


def update_live_db_file(filename):
    os.rename(filename, DB_FILE)


def main(args):
    force = '--force' in args
    ignore_git = '--ignore-git' in args
    db_info = download_db_info()
    if not db_info:
        return 'ERROR: Could not get database info'

    if not force:
        prev_data = get_prev_db_data()
        if prev_data and prev_data['checksum'] == db_info['checksum']:
            print('Checksums match. No update required.')
            return 0

        if prev_data and prev_data['updated'] > db_info['updated']:
            print('Remote database older than local. No update required.')
            return 0

        if not ignore_git:
            git_sha = get_git_sha()
            if git_sha != db_info['git_sha']:
                print('Git hashes do not match. No update required.')
                return 0

    new_db_file = db_info['file_name']
    download_db_file(new_db_file)
    checksum = get_db_checksum(new_db_file)
    if checksum == db_info['checksum']:
        update_live_db_file(new_db_file)
        set_db_data(db_info)
        print('Database successfully updated')
        return 0

    os.remove(new_db_file)
    return 'ERROR: Checksums do not match. Bad db download. Aborting.'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
