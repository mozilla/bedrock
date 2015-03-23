# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from subprocess import call
from django.test.utils import override_settings
from mock import patch

import chkcrontab_lib as chkcrontab
from funfactory.settings_base import path

from bedrock.base import geo
from bedrock.mozorg.tests import TestCase


CRONTAB_FILE_NAMES = ['bedrock-dev', 'bedrock-stage', 'bedrock-prod']
CRONTAB_FILES = [path('etc', 'cron.d', cf) for cf in CRONTAB_FILE_NAMES]


class TestCrontabFiles(TestCase):
    files_generated = False

    @classmethod
    def setUpClass(cls):
        for cron_file in CRONTAB_FILE_NAMES:
            call([path('bin', 'gen-crons.py'), '-t', cron_file, '-w', '/path/to/www',
                  '-s', '/path/to/src'])

    @classmethod
    def tearDownClass(cls):
        for cron_file in CRONTAB_FILE_NAMES:
            os.remove(path('etc', 'cron.d', cron_file))

    def test_crontab_files_have_newlines(self):
        """Crontab files should end with newline character."""
        for filename in CRONTAB_FILES:
            with open(filename) as cronfile:
                self.assertTrue(cronfile.read().endswith('\n'),
                                'No newline at end of ' + filename)

    def test_crontab_files_valid(self):
        """Crontab files should pass validation."""
        for filename in CRONTAB_FILES:
            cronlog = chkcrontab.LogCounter()
            return_value = chkcrontab.check_crontab(filename, cronlog)
            self.assertEqual(return_value, 0, 'Problem with ' + filename)


@patch('bedrock.base.geo.geo')
class TestGeo(TestCase):
    # real output from a real maxmind db
    good_geo_data = {
        u'continent': {
            u'code': u'NA',
            u'geoname_id': 6255149L,
            u'names': {u'de': u'Nordamerika',
                       u'en': u'North America',
                       u'es': u'Norteam\xe9rica',
                       u'fr': u'Am\xe9rique du Nord',
                       u'ja': u'\u5317\u30a2\u30e1\u30ea\u30ab',
                       u'pt-BR': u'Am\xe9rica do Norte',
                       u'ru': u'\u0421\u0435\u0432\u0435\u0440\u043d\u0430\u044f '
                              u'\u0410\u043c\u0435\u0440\u0438\u043a\u0430',
                       u'zh-CN': u'\u5317\u7f8e\u6d32'}
        },
        u'country': {
            u'geoname_id': 6252001L,
            u'iso_code': u'US',
            u'names': {u'de': u'USA',
                       u'en': u'United States',
                       u'es': u'Estados Unidos',
                       u'fr': u'\xc9tats-Unis',
                       u'ja': u'\u30a2\u30e1\u30ea\u30ab\u5408\u8846\u56fd',
                       u'pt-BR': u'Estados Unidos',
                       u'ru': u'\u0421\u0428\u0410',
                       u'zh-CN': u'\u7f8e\u56fd'}
        },
        u'location': {u'latitude': 38.0, u'longitude': -97.0},
        u'registered_country': {
            u'geoname_id': 6252001L,
            u'iso_code': u'US',
            u'names': {u'de': u'USA',
                       u'en': u'United States',
                       u'es': u'Estados Unidos',
                       u'fr': u'\xc9tats-Unis',
                       u'ja': u'\u30a2\u30e1\u30ea\u30ab\u5408\u8846\u56fd',
                       u'pt-BR': u'Estados Unidos',
                       u'ru': u'\u0421\u0428\u0410',
                       u'zh-CN': u'\u7f8e\u56fd'}
        }
    }

    def test_get_country_by_ip(self, geo_mock):
        geo_mock.get.return_value = self.good_geo_data
        self.assertEqual(geo.get_country_from_ip('1.1.1.1'), 'US')
        geo_mock.get.assert_called_with('1.1.1.1')

    @override_settings(MAXMIND_DEFAULT_COUNTRY='XX')
    def test_get_country_by_ip_default(self, geo_mock):
        """Geo failure should return default country."""
        geo_mock.get.return_value = None
        self.assertEqual(geo.get_country_from_ip('1.1.1.1'), 'XX')
        geo_mock.get.assert_called_with('1.1.1.1')

        geo_mock.reset_mock()
        geo_mock.get.side_effect = ValueError
        self.assertEqual(geo.get_country_from_ip('1.1.1.1'), 'XX')
        geo_mock.get.assert_called_with('1.1.1.1')

    @override_settings(MAXMIND_DEFAULT_COUNTRY='XX')
    def test_get_country_by_ip_bad_data(self, geo_mock):
        """Bad data from geo should return default country."""
        geo_mock.get.return_value = {'fred': 'flintstone'}
        self.assertEqual(geo.get_country_from_ip('1.1.1.1'), 'XX')
        geo_mock.get.assert_called_with('1.1.1.1')
