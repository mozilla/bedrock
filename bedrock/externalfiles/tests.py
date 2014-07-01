# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime

from django.conf import settings

from mock import patch

from bedrock import externalfiles
from bedrock.mozorg.tests import TestCase


class TestExternalFile(TestCase):
    def setUp(self):
        settings.EXTERNAL_FILES['test'] = {
            'url': 'http://www.mozilla.org/keymaster/gatekeeper/there.is.only.xul',
        }

    def tearDown(self):
        del settings.EXTERNAL_FILES['test']

    def test_file_name(self):
        """Should be based on URL if not provided."""
        self.assertEqual(externalfiles.ExternalFile('test').name, 'there.is.only.xul')

    def test_file_name_provided(self):
        """Should be based on URL if not provided."""
        filename = 'there.is.no.data.xul'
        settings.EXTERNAL_FILES['test']['name'] = filename
        self.assertEqual(externalfiles.ExternalFile('test').name, filename)

    @patch.object(externalfiles, 'open', create=True)
    def test_last_modified(self, open_mock):
        """Should return the modified timestamp."""
        open_mock.return_value.__enter__.return_value.read.return_value = 'The Dude abides.'
        self.assertEqual(externalfiles.ExternalFile('test').last_modified, 'The Dude abides.')

    @patch.object(externalfiles, 'open', create=True)
    def test_last_modified_read_error(self, open_mock):
        """Should return None on file read error."""
        open_mock.return_value.__enter__.return_value.read.side_effect = IOError
        self.assertIsNone(externalfiles.ExternalFile('test').last_modified)

    @patch.object(externalfiles, 'open', create=True)
    def test_last_modified_datetime(self, open_mock):
        """should properly convert stored date stamp to datetime."""
        read_mock = open_mock.return_value.__enter__.return_value.read
        read_mock.return_value = 'Tue, 08 Jul 2014 12:00:00 GMT'
        good_datetime = datetime(year=2014, month=7, day=8, hour=12)
        self.assertEqual(externalfiles.ExternalFile('test').last_modified_datetime,
                         good_datetime)

    @patch.object(externalfiles, 'open', create=True)
    def test_last_modified_datetime_error(self, open_mock):
        """Should return None on error."""
        open_mock.return_value.__enter__.return_value.read.side_effect = IOError
        self.assertIsNone(externalfiles.ExternalFile('test').last_modified_datetime)

    @patch.object(externalfiles, 'open', create=True)
    def test_last_modified_datetime_bad_str(self, open_mock):
        """Should return None with bad date string."""
        open_mock.return_value.__enter__.return_value.read.return_value = 'The Dude abides.'
        self.assertIsNone(externalfiles.ExternalFile('test').last_modified_datetime)
