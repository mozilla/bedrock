# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import codecs
import logging
from os import mkdir
from os.path import abspath, basename, dirname, exists, join
from datetime import datetime

from django.conf import settings
from django.utils.functional import cached_property
from django.utils.http import parse_http_date_safe

import requests


log = logging.getLogger(__name__)
FILES_PATH = join(dirname(abspath(__file__)), 'files_cache')
UPDATED_FILE = '{0}.updated.txt'


class SVNFile(object):
    def __init__(self, file_id):
        fileinfo = settings.SVN_FILES.get(file_id, None)
        if fileinfo is None:
            raise ValueError('No SVN file with the {0} ID.'.format(file_id))

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

        try:
            resp = requests.get(self.url, headers=headers, verify=True)
        except requests.RequestException:
            log.exception('Error connecting to %s' % self.url)
            return

        if resp.status_code == 304:
            log.info('{0} already up-to-date.'.format(self.name))

        elif resp.status_code == 200:
            # make sure cache dir exists
            if not exists(FILES_PATH):
                try:
                    mkdir(FILES_PATH, 0777)
                except OSError:
                    pass

            with codecs.open(self.file_path, 'wb', 'utf8') as fh:
                fh.write(resp.text)

            with open(self.updated_file_path, 'wb') as lu_fh:
                lu_fh.write(resp.headers['last-modified'])

            log.info('Successfully updated {0}.'.format(self.name))

        else:
            log.error('Unknown error occurred updating {0} ({1}): {2}'.format(self.name,
                                                                              resp.status_code,
                                                                              resp.text))
