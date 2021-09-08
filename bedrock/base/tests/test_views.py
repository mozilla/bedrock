import json
from unittest.mock import patch

from django.test import TestCase, RequestFactory
from django.test import override_settings

from bedrock.base.views import geolocate, GeoRedirectView


class TestGeolocate(TestCase):
    def get_country(self, country):
        with patch('bedrock.base.views.get_country_from_request') as geo_mock:
            geo_mock.return_value = country, 'local'
            rf = RequestFactory()
            req = rf.get('/')
            resp = geolocate(req)
            return json.loads(resp.content)

    def test_geo_returns(self):
        self.assertDictEqual(self.get_country('US'), {'country_code': 'US',
                                                      'data_source': 'local'})
        self.assertDictEqual(self.get_country('FR'), {'country_code': 'FR',
                                                      'data_source': 'local'})
        self.assertDictEqual(self.get_country(None), {
            "error": {
                "errors": [{
                    "domain": "geolocation",
                    "reason": "notFound",
                    "message": "Not found",
                }],
                "code": 404,
                "message": "Not found",
            }
        })


geo_view = GeoRedirectView.as_view(
    geo_urls={
        'CA': 'firefox.new',
        'US': 'firefox',
    },
    default_url='https://abide.dude'
)


@override_settings(DEV=False)
class TestGeoRedirectView(TestCase):
    def get_response(self, country):
        with patch('bedrock.base.views.get_country_from_request') as geo_mock:
            geo_mock.return_value = country, 'local'
            rf = RequestFactory()
            req = rf.get('/')
            return geo_view(req)

    def test_special_country(self):
        resp = self.get_response('CA')
        assert resp.status_code == 302
        assert resp['location'] == '/firefox/new/'

        resp = self.get_response('US')
        assert resp.status_code == 302
        assert resp['location'] == '/firefox/'

    def test_other_country(self):
        resp = self.get_response('DE')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'

        resp = self.get_response('JA')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'

    def test_invalid_country(self):
        resp = self.get_response('dude')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'

        resp = self.get_response('42')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'
