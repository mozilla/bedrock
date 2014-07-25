# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from datetime import datetime

from django.conf import settings

from mock import Mock, patch

from bedrock import externalfiles
from bedrock.mozorg.tests import TestCase
import requests


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

    @patch.object(externalfiles, 'requests')
    def test_update_adds_headers(self, requests_mock):
        """Should add proper modified headers when possible."""
        requests_mock.get.side_effect = requests.RequestException
        ef = externalfiles.ExternalFile('test')
        modified_str = 'Willlllmaaaaaaa!!'
        ef.last_modified = modified_str
        try:
            ef.update()
        except requests.RequestException:
            pass
        requests_mock.get.called_once_with(settings.EXTERNAL_FILES['test']['url'],
                                           headers={'if-modified-since': modified_str},
                                           verify=True)

    @patch.object(externalfiles, 'requests')
    def test_update_force_not_add_headers(self, requests_mock):
        """Should not add proper modified headers when force is True."""
        requests_mock.get.side_effect = requests.RequestException
        ef = externalfiles.ExternalFile('test')
        ef.last_modified = 'YabbaDabbaDooo!!'
        try:
            ef.update(force=True)
        except requests.RequestException:
            pass
        requests_mock.get.called_once_with(settings.EXTERNAL_FILES['test']['url'], headers={},
                                           verify=True)

    def test_validate_resp_200(self):
        """Should return the content for a successful request."""
        response = Mock(status_code=200, text='Huge Success')
        ef = externalfiles.ExternalFile('test')
        self.assertEqual(ef.validate_resp(response), 'Huge Success')

    def test_validate_resp_304(self):
        """Should return None if the URL is up-to-date."""
        response = Mock(status_code=304)
        ef = externalfiles.ExternalFile('test')
        self.assertIsNone(ef.validate_resp(response))

    def test_validate_resp_404(self):
        """Should raise an exception for a missing file."""
        response = Mock(status_code=404)
        ef = externalfiles.ExternalFile('test')
        with self.assertRaisesMessage(ValueError, 'File not found (404): ' + ef.name):
            ef.validate_resp(response)

    def test_validate_resp_500(self):
        """Should raise an exception for all other codes."""
        response = Mock(status_code=500)
        ef = externalfiles.ExternalFile('test')
        with self.assertRaises(ValueError) as e:
            ef.validate_resp(response)

        self.assertTrue(str(e.exception).startswith('Unknown error'))
