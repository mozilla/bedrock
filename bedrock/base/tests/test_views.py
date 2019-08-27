import json

from django.test import TestCase, RequestFactory
from django.test import override_settings

from bedrock.base.views import geolocate, GeoRedirectView


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
        rf = RequestFactory()
        req = rf.get('/', HTTP_CF_IPCOUNTRY=country)
        return geo_view(req)

    def test_special_country(self):
        resp = self.get_response('CA')
        assert resp.status_code == 302
        assert resp['location'] == '/firefox/new/'
        assert resp['cache-control'] == 'max-age=0, no-cache, no-store, must-revalidate'

        resp = self.get_response('US')
        assert resp.status_code == 302
        assert resp['location'] == '/firefox/'
        assert resp['cache-control'] == 'max-age=0, no-cache, no-store, must-revalidate'

    def test_other_country(self):
        resp = self.get_response('DE')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'
        assert resp['cache-control'] == 'max-age=0, no-cache, no-store, must-revalidate'

        resp = self.get_response('JA')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'
        assert resp['cache-control'] == 'max-age=0, no-cache, no-store, must-revalidate'

    def test_invalid_country(self):
        resp = self.get_response('dude')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'
        assert resp['cache-control'] == 'max-age=0, no-cache, no-store, must-revalidate'

        resp = self.get_response('42')
        assert resp.status_code == 302
        assert resp['location'] == 'https://abide.dude'
        assert resp['cache-control'] == 'max-age=0, no-cache, no-store, must-revalidate'
