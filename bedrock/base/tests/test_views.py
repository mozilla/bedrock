import json

from django.test import TestCase, RequestFactory
from django.test import override_settings

from bedrock.base.views import geolocate


class TestGeolocate(TestCase):
    def get_country(self, country):
        rf = RequestFactory()
        req = rf.get('/', HTTP_CF_IPCOUNTRY=country)
        resp = geolocate(req)
        return json.loads(resp.content)

    @override_settings(DEV=False)
    def test_cdn_header(self):
        self.assertDictEqual(self.get_country('US'), {'country_code': 'US'})
        self.assertDictEqual(self.get_country('FR'), {'country_code': 'FR'})
        self.assertDictEqual(self.get_country('XX'), {
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

    @override_settings(DEV=True, DEV_GEO_COUNTRY_CODE='DE')
    def test_dev_mode(self):
        # should match the setting in DEV mode
        self.assertDictEqual(self.get_country('US'), {'country_code': 'DE'})
