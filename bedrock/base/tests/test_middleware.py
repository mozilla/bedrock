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
        self.assertEqual(resp['Location'], '/de' + path + '?icn=locale')

    @override_settings(DEV_LANGUAGES=('de', 'fr'),
                       FF_EXEMPT_LANG_PARAM_URLS=())
    def test_redirects_to_correct_language_with_qs(self):
        """Should redirect to lang prefixed url, preserving query string."""
        path = '/the/dude/?abiding=true'
        req = self.rf.get(path, HTTP_ACCEPT_LANGUAGE='de')
        resp = LocaleURLMiddleware().process_request(req)
        self.assertEqual(resp['Location'], '/de' + path + '&icn=locale')

    @override_settings(DEV_LANGUAGES=('de', 'fr'),
                       FF_EXEMPT_LANG_PARAM_URLS=())
    def test_lang_redirect_no_dupe_icn(self):
        """Should redirect to lang prefixed url and avoid duplicating icn param."""
        path = '/the/dude/?icn=locale'
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
        self.assertEqual(resp['Location'], '/en-US' + path + '?icn=locale')

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

    @override_settings(DEV_LANGUAGES=('de', 'fr'),
                       FF_EXEMPT_LANG_PARAM_URLS=())
    def test_redirects_to_correct_language_despite_unicode_errors(self):
        """Should redirect to lang prefixed url, stripping invalid chars."""
        path = '/the/dude/'
        corrupt_querystring = '?a\xa4\x91b\xa4\x91i\xc0de=s'
        corrected_querystring = '?abide=s'
        req = self.rf.get(path + corrupt_querystring,
                          HTTP_ACCEPT_LANGUAGE='de')
        resp = LocaleURLMiddleware().process_request(req)
        self.assertEqual(resp['Location'],
                         '/de' + path + corrected_querystring + '&icn=locale')
