import json
from hashlib import sha256
from os import getenv
from subprocess import check_output, CalledProcessError


JSON_DATA_FILE = getenv('AWS_DB_JSON_DATA_FILE', 'bedrock_db_info.json')
DB_FILE = 'bedrock.db'
CACHE = {}
BLOCKSIZE = 65536


def _sha256_sum(filename):
    hasher = sha256()
    with open(filename, 'rb') as fh:
        for chunk in iter(lambda: fh.read(BLOCKSIZE), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def get_db_checksum(filename=None):
    filename = filename or DB_FILE
    cache_key = 'db_sum_%s' % filename
    db_sum = CACHE.get(cache_key)
    if not db_sum:
        db_sum = _sha256_sum(filename)
        CACHE[cache_key] = db_sum

    return db_sum


def get_git_sha():
    git_sha = CACHE.get('git_sha')
    if not git_sha:
        git_sha = getenv('GIT_SHA')
        if not git_sha:
            try:
                git_sha = check_output('git rev-parse HEAD', shell=True).strip()
            except CalledProcessError:
                git_sha = 'testing'

        CACHE['git_sha'] = git_sha

    return git_sha


def get_prev_db_data():
    try:
        with open(JSON_DATA_FILE, 'r') as fp:
            return json.load(fp)
    except IOError:
        # file does not exist
        return None


def set_db_data(db_data):
    with open(JSON_DATA_FILE, 'w') as fp:
        json.dump(db_data, fp)
