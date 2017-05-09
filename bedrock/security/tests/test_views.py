# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mock import patch
from nose.tools import eq_, ok_
from product_details import product_details
from product_details.version_compare import Version

from bedrock.mozorg.tests import TestCase
from bedrock.security.models import Product
from bedrock.security.views import ProductView, ProductVersionView, product_is_obsolete


@patch.object(product_details, 'firefox_versions', {'LATEST_FIREFOX_VERSION': '33.0',
                                                    'FIREFOX_ESR': '31.2.0'})
@patch.object(product_details, 'thunderbird_versions', {'LATEST_THUNDERBIRD_VERSION': '31.2.0'})
def test_product_is_obsolete():
    ok_(product_is_obsolete('firefox', '3.6'))
    ok_(product_is_obsolete('firefox', '32'))
    ok_(product_is_obsolete('firefox-esr', '17.0'))
    ok_(product_is_obsolete('thunderbird', '30'))
    ok_(product_is_obsolete('seamonkey', '2.0'))
    ok_(product_is_obsolete('seamonkey', '2.19'))
    ok_(product_is_obsolete('other-things', '3000'))

    ok_(not product_is_obsolete('firefox', '33.0.2'))
    ok_(not product_is_obsolete('firefox', '34.0'))
    ok_(not product_is_obsolete('firefox-esr', '31.0'))
    ok_(not product_is_obsolete('thunderbird', '31'))
    ok_(not product_is_obsolete('seamonkey', '2.30'))


class TestViews(TestCase):
    def setUp(self):
        pvnames = [
            'Firefox 3.6',
            'Firefox 4.0',
            'Firefox 4.0.1',
            'Firefox 4.2',
            'Firefox 4.2.3',
            'Firefox 24.0',
        ]
        self.pvs = [Product.objects.create(name=pv) for pv in pvnames]

    def test_product_view_min_version(self):
        """Should not include versions below minimum."""
        pview = ProductView()
        pview.kwargs = {'slug': 'firefox'}
        with patch.dict(pview.minimum_versions, {'firefox': Version('4.2')}):
            self.assertListEqual(pview.get_queryset(),
                                 [self.pvs[5], self.pvs[4], self.pvs[3]])

        with patch.dict(pview.minimum_versions, {'firefox': Version('22.0')}):
            self.assertListEqual(pview.get_queryset(), [self.pvs[5]])

    def test_product_version_view_filter_major(self):
        """Given a major version should return all minor versions."""
        pview = ProductVersionView()
        pview.kwargs = {'product': 'firefox', 'version': '4'}
        self.assertListEqual(pview.get_queryset(),
                             [self.pvs[4], self.pvs[3], self.pvs[2], self.pvs[1]])

    def test_product_version_view_filter_minor(self):
        """Given a minor version should return all point versions."""
        pview = ProductVersionView()
        pview.kwargs = {'product': 'firefox', 'version': '4.2'}
        self.assertListEqual(pview.get_queryset(), [self.pvs[4], self.pvs[3]])


class TestKVRedirects(TestCase):
    def _test_names(self, url_component, expected):
        # old urls lack '/en-US' prefix, but that will be the first redirect.
        path = '/en-US/security/known-vulnerabilities/{0}.html'.format(url_component)
        resp = self.client.get(path)
        eq_(resp.status_code, 301)
        eq_(expected, resp['Location'].split('/')[-2])

    def test_correct_redirects(self):
        self._test_names('firefox', 'firefox')
        self._test_names('firefoxESR', 'firefox-esr')
        self._test_names('firefox20', 'firefox-2.0')
        self._test_names('thunderbird15', 'thunderbird-1.5')
        self._test_names('suite17', 'mozilla-suite')

    def test_spaces_removed(self):
        """Should succeed even if accidental spaces are in the URL.

        Bug 1171181.
        """
        self._test_names('firefox3%20%200', 'firefox-3.0')

    def test_unknown_is_404(self):
        """Should 410 instead of 500 if an unknown url matches the redirector.

        Bug 1171181.
        """
        path = '/en-US/security/known-vulnerabilities/the-dude-abides-15.html'
        resp = self.client.get(path)
        eq_(resp.status_code, 410)


class TestOldAdvisories(TestCase):
    def _test_redirect(self, path, expected):
        # old urls lack '/en-US' prefix, but that will be the first redirect.
        resp = self.client.get('/en-US' + path)
        eq_(resp.status_code, 301)
        ok_(resp['Location'].endswith(expected))

    def test_old_urls(self):
        """Should redirect old URLs properly."""
        self._test_redirect('/security/announce/mfsa2005-31.html',
                            '/security/advisories/mfsa2005-31/')
        self._test_redirect('/security/announce/2005/mfsa2005-40.html',
                            '/security/advisories/mfsa2005-40/')
        self._test_redirect('/security/advisories/2008/mfsa2008-47.html',
                            '/security/advisories/mfsa2008-47/')
        self._test_redirect('/security/advisories/mfsa2008-66/mfsa2008-37.html',
                            '/security/advisories/mfsa2008-37/')
