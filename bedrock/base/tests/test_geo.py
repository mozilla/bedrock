# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.test import RequestFactory
from django.test.utils import override_settings

from mock import patch

from bedrock.base import geo
from bedrock.mozorg.tests import TestCase


@patch("bedrock.base.geo._get_geo_client")
class TestGeo(TestCase):
    # real output from a real maxmind db
    good_geo_data = {
        "continent": {
            "code": "NA",
            "geoname_id": 6255149,
            "names": {
                "de": "Nordamerika",
                "en": "North America",
                "es": "Norteamérica",
                "fr": "Amérique du Nord",
                "ja": "北アメリカ",
                "pt-BR": "América do Norte",
                "ru": "Северная Америка",
                "zh-CN": "北美洲",
            },
        },
        "country": {
            "geoname_id": 6252001,
            "iso_code": "US",
            "names": {
                "de": "USA",
                "en": "United States",
                "es": "Estados Unidos",
                "fr": "États-Unis",
                "ja": "アメリカ合衆国",
                "pt-BR": "Estados Unidos",
                "ru": "США",
                "zh-CN": "美国",
            },
        },
        "registered_country": {
            "geoname_id": 6252001,
            "iso_code": "US",
            "names": {
                "de": "USA",
                "en": "United States",
                "es": "Estados Unidos",
                "fr": "États-Unis",
                "ja": "アメリカ合衆国",
                "pt-BR": "Estados Unidos",
                "ru": "США",
                "zh-CN": "美国",
            },
        },
    }

    def test_get_country_by_ip(self, geo_mock):
        geo_mock.return_value.get.return_value = self.good_geo_data
        self.assertEqual(geo.get_country_from_ip('1.1.1.1'), 'US')
        geo_mock.return_value.get.assert_called_with('1.1.1.1')

    def test_get_country_by_ip_default(self, geo_mock):
        """Geo failure should return default country."""
        geo_mock.return_value.get.return_value = None
        self.assertIsNone(geo.get_country_from_ip('1.1.1.1'))
        geo_mock.return_value.get.assert_called_with('1.1.1.1')

        geo_mock.reset_mock()
        geo_mock.return_value.get.side_effect = ValueError
        self.assertIsNone(geo.get_country_from_ip('1.1.1.1'))
        geo_mock.return_value.get.assert_called_with('1.1.1.1')

    def test_get_country_by_ip_bad_data(self, geo_mock):
        """Bad data from geo should return None."""
        geo_mock.return_value.get.return_value = {'fred': 'flintstone'}
        self.assertIsNone(geo.get_country_from_ip('1.1.1.1'))
        geo_mock.return_value.get.assert_called_with('1.1.1.1')

    @override_settings(DEV=True, MAXMIND_DEFAULT_COUNTRY='XX')
    def test_get_country_by_ip_dev_mode(self, geo_mock):
        geo_mock.return_value = None
        assert geo.get_country_from_ip('1.1.1.1') == 'XX'

    def test_get_country_from_maxmind(self, geo_mock):
        geo_mock.return_value.get.return_value = self.good_geo_data
        req = RequestFactory().get('/', HTTP_X_FORWARDED_FOR='192.168.1.2, 192.168.8.8')
        self.assertEqual(geo.get_country_from_maxmind(req), 'US')
        geo_mock.return_value.get.assert_called_with('192.168.1.2')

    def test_get_country_from_maxmind_single_ip(self, geo_mock):
        geo_mock.return_value.get.return_value = self.good_geo_data
        req = RequestFactory().get('/', HTTP_X_FORWARDED_FOR='192.168.8.8')
        self.assertEqual(geo.get_country_from_maxmind(req), 'US')
        geo_mock.return_value.get.assert_called_with('192.168.8.8')

    def test_get_country_from_maxmind_no_header(self, geo_mock):
        geo_mock.return_value.get.return_value = self.good_geo_data
        req = RequestFactory().get('/')
        self.assertEqual(geo.get_country_from_maxmind(req), None)
        geo_mock.return_value.get.assert_not_called()
