# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
from os.path import basename
from time import mktime
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.conf import settings
from django.core.cache import caches
from django.utils.http import http_date

import requests

from bedrock.externalfiles.models import ExternalFile as EFModel


log = logging.getLogger(__name__)


class ExternalFile(object):
    def __init__(self, file_id):
        try:
            fileinfo = settings.EXTERNAL_FILES[file_id]
        except KeyError:
            raise ValueError('No external file with the {0} ID.'.format(file_id))

        self._cache = caches['externalfiles']
        self.file_id = file_id
        self.url = fileinfo['url']
        self.name = fileinfo.get('name', basename(self.url))
        self.cache_key = 'externalfile:{}'.format(self.file_id)

    @property
    def file_object(self):
        efo = self._cache.get(self.cache_key)
        if not efo:
            try:
                efo = EFModel.objects.get(name=self.file_id)
            except EFModel.DoesNotExist:
                pass
            else:
                self._cache.set(self.cache_key, efo, 3600)  # 1 hour

        return efo

    @property
    def last_modified(self):
        """
        Return the last-modified header from the most recent names update.
        :return: str timestamp
        """
        fo = self.file_object
        if fo:
            return fo.last_modified

        return None

    @property
    def last_modified_http(self):
        """
        Return last modified date as a properly formatted string suitable for HTTP headers.
        """
        return http_date(mktime(self.last_modified.timetuple()))

    def last_modified_callback(self, *args, **kwargs):
        """
        To be used as the argument for the `last_modified` view decorator.
        """
        return self.last_modified

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
        return self.file_object.content.encode('utf-8')

    def readlines(self):
        return StringIO(self.read()).readlines()

    def update(self, force=False):
        log.info('Updating {0}.'.format(self.name))
        headers = {}
        if not force:
            if self.last_modified:
                headers['if-modified-since'] = self.last_modified_http

        resp = requests.get(self.url, headers=headers, verify=True)
        content = self.validate_resp(resp)

        if content is None:
            # up-to-date
            return None

        fo = self.file_object
        if fo:
            fo.content = content
            fo.save()
        else:
            EFModel.objects.create(name=self.file_id, content=content)

        log.info('Successfully updated {0}.'.format(self.name))
        return True

    def clear_cache(self):
        self._cache.delete(self.cache_key)
