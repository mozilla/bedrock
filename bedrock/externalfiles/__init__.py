# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import codecs
import logging
from os import mkdir
from os.path import abspath, basename, dirname, exists, join
from datetime import datetime

from django.conf import settings
from django.core.cache import get_cache, InvalidCacheBackendError
from django.utils.functional import cached_property
from django.utils.http import parse_http_date_safe

import requests


log = logging.getLogger(__name__)
FILES_PATH = join(dirname(abspath(__file__)), 'files_cache')
UPDATED_FILE = '{0}.updated.txt'


class ExternalFile(object):
    cache_key = None

    def __init__(self, file_id):
        try:
            fileinfo = settings.EXTERNAL_FILES[file_id]
        except KeyError:
            raise ValueError('No external file with the {0} ID.'.format(file_id))

        try:
            self._cache = get_cache('externalfiles')
        except InvalidCacheBackendError:
            self._cache = get_cache('default')

        self.file_id = file_id
        self.url = fileinfo['url']
        self.name = fileinfo.get('name', basename(self.url))
        self.updated_name = UPDATED_FILE.format(self.name)
        self.file_path = join(FILES_PATH, self.name)
        self.updated_file_path = join(FILES_PATH, self.updated_name)

    @cached_property
    def last_modified(self):
        """
        Return the last-modified header from the most recent names update.
        :return: str timestamp
        """
        try:
            with open(self.updated_file_path) as lu_fh:
                return lu_fh.read().strip()
        except IOError:
            return None

    @cached_property
    def last_modified_datetime(self):
        """
        Return the last-modified header from the most recent names update as datetime.
        :return: datetime (or None on error)
        """
        if self.last_modified:
            date_epoch = parse_http_date_safe(self.last_modified)
            if date_epoch:
                return datetime.utcfromtimestamp(date_epoch)

        return None

    def last_modified_callback(self, *args, **kwargs):
        """
        To be used as the argument for the `last_modified` view decorator.
        """
        return self.last_modified_datetime

    def validate_resp(self, resp):
        """
        Validate the response from the server, returning the content.
        :param resp: requests.Response
        :return: str or None
        :raises: ValueError
        """
        if resp.status_code == 304:
            log.info('{0} already up-to-date.'.format(self.name))
            return None

        if resp.status_code == 200:
            content = resp.text
            if not content:
                raise ValueError('No content returned')

            if hasattr(self, 'validate_content'):
                return self.validate_content(content)

            return content

        if resp.status_code == 404:
            raise ValueError('File not found (404): ' + self.name)

        raise ValueError('Unknown error occurred updating {0} ({1}): {2}'.format(self.name,
                                                                                 resp.status_code,
                                                                                 resp.text))

    def read(self):
        with open(self.file_path, 'rb') as fh:
            return fh.read()

    def readlines(self):
        with open(self.file_path, 'rb') as fh:
            return fh.readlines()

    def update(self, force=False):
        log.info('Updating {0}.'.format(self.name))
        headers = {}
        if not force:
            if self.last_modified:
                headers['if-modified-since'] = self.last_modified

        resp = requests.get(self.url, headers=headers, verify=True)
        content = self.validate_resp(resp)

        if content is None:
            # up-to-date
            return None

        # make sure cache dir exists
        if not exists(FILES_PATH):
            try:
                mkdir(FILES_PATH, 0777)
            except OSError:
                # already exists
                pass

        with codecs.open(self.file_path, 'wb', 'utf8') as fh:
            fh.write(content)

        with open(self.updated_file_path, 'wb') as lu_fh:
            lu_fh.write(resp.headers['last-modified'])

        log.info('Successfully updated {0}.'.format(self.name))
        return True

    def clear_cache(self):
        if self.cache_key:
            self._cache.delete(self.cache_key)
