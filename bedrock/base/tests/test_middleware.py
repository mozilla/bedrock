from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from bedrock.base.middleware import LocaleURLMiddleware


@override_settings(DEV=True)
class TestLocaleURLMiddleware(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.middleware = LocaleURLMiddleware()

    @override_settings(DEV_LANGUAGES=('de', 'fr'),
                       FF_EXEMPT_LANG_PARAM_URLS=())
    def test_redirects_to_correct_language(self):
        """Should redirect to lang prefixed url."""
        path = '/the/dude/'
        req = self.rf.get(path, HTTP_ACCEPT_LANGUAGE='de')
        resp = LocaleURLMiddleware().process_request(req)
        self.assertEqual(resp['Location'], '/de' + path)

    @override_settings(DEV_LANGUAGES=('es', 'fr'),
                       LANGUAGE_CODE='en-US',
                       FF_EXEMPT_LANG_PARAM_URLS=())
    def test_redirects_to_default_language(self):
        """Should redirect to default lang if not in settings."""
        path = '/the/dude/'
        req = self.rf.get(path, HTTP_ACCEPT_LANGUAGE='de')
        resp = LocaleURLMiddleware().process_request(req)
        self.assertEqual(resp['Location'], '/en-US' + path)

    @override_settings(DEV_LANGUAGES=('de', 'fr'),
                       FF_EXEMPT_LANG_PARAM_URLS=('/other/',))
    def test_redirects_lang_param(self):
        """Middleware should remove the lang param on redirect."""
        path = '/fr/the/dude/'
        req = self.rf.get(path, {'lang': 'de'})
        resp = LocaleURLMiddleware().process_request(req)
        self.assertEqual(resp['Location'], '/de/the/dude/')

    @override_settings(DEV_LANGUAGES=('de', 'fr'),
                       FF_EXEMPT_LANG_PARAM_URLS=('/dude/',))
    def test_no_redirect_lang_param(self):
        """Middleware should not redirect when exempt."""
        path = '/fr/the/dude/'
        req = self.rf.get(path, {'lang': 'de'})
        resp = LocaleURLMiddleware().process_request(req)
        self.assertIs(resp, None)  # no redirect
