import json

from django.http import HttpResponse
from django.test import TestCase, RequestFactory
from django.test import override_settings

from mock import patch

from bedrock.base import views
from bedrock.base.views import geolocate, cron_health_check


HEALTH_FILES = (
    ('go_bowling', 10 * 60),
    ('abide', 60 * 60),
)


@patch('bedrock.base.views.render', return_value=HttpResponse())
@patch('bedrock.base.views.os.path.getmtime')
@patch('bedrock.base.views.time')
class CronHealthCheckTests(TestCase):
    def setUp(self):
        self.old_health = views.HEALTH_FILES
        views.HEALTH_FILES = HEALTH_FILES

    def tearDown(self):
        views.HEALTH_FILES = self.old_health

    def request(self):
        return RequestFactory().get('/')

    def test_check_pass(self, time_mock, mtime_mock, render_mock):
        mtime_mock.return_value = 100
        time_mock.return_value = 100
        cron_health_check(self.request())
        assert render_mock.call_args[1]['status'] == 200
        assert render_mock.call_args[0][2]['results'] == [
            ('go_bowling', 600, 0, True),
            ('abide', 3600, 0, True),
        ]

    def test_check_fail(self, time_mock, mtime_mock, render_mock):
        mtime_mock.return_value = 100
        time_mock.return_value = 1100
        cron_health_check(self.request())
        assert render_mock.call_args[1]['status'] == 500
        assert render_mock.call_args[0][2]['results'] == [
            ('go_bowling', 600, 1000, False),
            ('abide', 3600, 1000, True),
        ]

    def test_missing_files(self, time_mock, mtime_mock, render_mock):
        mtime_mock.side_effect = OSError()
        cron_health_check(self.request())
        time_mock.assert_not_called()
        assert render_mock.call_args[1]['status'] == 500
        assert render_mock.call_args[0][2]['results'] == [
            ('go_bowling', 600, 'None', False),
            ('abide', 3600, 'None', False),
        ]


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
