from urlparse import parse_qs, urlparse

from django.conf import settings
from django.test.client import RequestFactory

from django_jinja.backend import Jinja2
from nose.tools import eq_, ok_
from pyquery import PyQuery as pq

from product_details import product_details
from bedrock.mozorg.tests import TestCase

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


class TestDownloadButtons(TestCase):

    def latest_version(self):
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_desktop_links(self, links):
        """Desktop links should have the correct firefox version"""
        # valid product strings
        keys = [
            'firefox-%s' % self.latest_version(),
            'firefox-stub',
            'firefox-latest-ssl',
            'firefox-beta-stub',
            'firefox-beta-latest-ssl',
        ]

        for link in links:
            url = pq(link).attr('href')
            ok_(any(key in url for key in keys))

    def check_dumb_button(self, doc):
        # Make sure 5 links are present
        links = doc('li a')
        eq_(links.length, 5)

        self.check_desktop_links(links[:4])

        # Check that the rest of the links are Android and iOS
        eq_(pq(links[4]).attr('href'), settings.GOOGLE_PLAY_FIREFOX_LINK)
        eq_(pq(links[5]).attr('href'),
            settings.APPLE_APPSTORE_FIREFOX_LINK.replace('/{country}/', '/'))

    def test_button_force_direct(self):
        """
        If the force_direct parameter is True, all download links must be
        directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(force_direct=true) }}",
                        {'request': get_request}))

        # Check that the first 5 links are direct.
        links = doc('.download-list a')

        for link in links[:5]:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['fr'])
            # direct links should not have the data attr.
            ok_(link.attr('data-direct-link') is None)

    def test_button_locale_in_transition(self):
        """
        If the locale_in_transition parameter is True, the link to scene2 should include the locale
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(locale_in_transition=true) }}",
                        {'request': get_request}))

        links = doc('.download-list a')

        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            eq_(href, '/fr/firefox/download/thanks/')

        doc = pq(render("{{ download_firefox(locale_in_transition=false) }}",
                        {'request': get_request}))

        links = doc('.download-list a')

        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            eq_(href, '/firefox/download/thanks/')

    def test_download_location_attribute(self):
        """
        If the download_location parameter is set, it should be included as a data attribute.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(download_location='primary cta') }}",
                        {'request': get_request}))

        links = doc('.download-list a')

        for link in links:
            link = pq(link)
            eq_(link.attr('data-download-location'), 'primary cta')

        doc = pq(render("{{ download_firefox() }}", {'request': get_request}))

        links = doc('.download-list a')

        for link in links[1:5]:
            link = pq(link)
            ok_(link.attr('data-download-location') is None)

    def test_button_has_data_attr_if_not_direct(self):
        """
        If the button points to the thank you page, it should have a
        `data-direct-link` attribute that contains the direct url.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox() }}",
                        {'request': get_request}))

        # The first 5 links should be for desktop.
        links = doc('.download-list a')

        for link in links[:5]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))

        # The seventh link is mobile and should not have the attr
        ok_(pq(links[5]).attr('data-direct-link') is None)

    def test_nightly_desktop(self):
        """
        The Nightly channel should have the Windows universal stub installer
        instead of the Windows 64-bit build
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('nightly', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux64')
        eq_(pq(list[3]).attr('class'), 'os_linux')
        # stub disabled for now for non-en-US locales
        # bug 1339870
        # ok_('stub' in pq(pq(list[1]).find('a')[0]).attr('href'))

    def test_aurora_desktop(self):
        """The Aurora channel should have Windows 64 build"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_win64')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_osx')
        eq_(pq(list[3]).attr('class'), 'os_linux64')
        eq_(pq(list[4]).attr('class'), 'os_linux')

    def test_beta_desktop(self):
        """The Beta channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('beta', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_win64')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_osx')
        eq_(pq(list[3]).attr('class'), 'os_linux64')
        eq_(pq(list[4]).attr('class'), 'os_linux')

    def test_firefox_desktop(self):
        """The Release channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_win64')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_osx')
        eq_(pq(list[3]).attr('class'), 'os_linux64')
        eq_(pq(list[4]).attr('class'), 'os_linux')

    def test_latest_nightly_android(self):
        """The download button should have a Google Play link"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('nightly', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        links = doc('.download-list li a')
        eq_(links.length, 1)
        ok_(pq(links[0]).attr('href').startswith('https://play.google.com'))

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_beta_mobile(self):
        """The download button should have a Google Play link"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('beta', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        links = doc('.download-list li a')
        eq_(links.length, 1)
        ok_(pq(links[0]).attr('href').startswith('https://play.google.com'))

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_firefox_mobile(self):
        """The download button should have a Google Play link"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox(platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        links = doc('.download-list li a')
        eq_(links.length, 1)
        ok_(pq(links[0]).attr('href').startswith('https://play.google.com'))

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_ios(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox(platform='ios') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_ios')


class TestDownloadList(TestCase):

    def latest_version(self):
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_desktop_links(self, links):
        """Desktop links should have the correct firefox version"""
        # valid product strings
        keys = [
            'firefox-%s' % self.latest_version(),
            'firefox-stub',
            'firefox-latest-ssl',
            'firefox-beta-stub',
            'firefox-beta-latest-ssl',
        ]

        for link in links:
            url = pq(link).attr('href')
            ok_(any(key in url for key in keys))

    def test_firefox_desktop_list_release(self):
        """
        All release download links must be directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox_desktop_list() }}",
                        {'request': get_request}))

        # Check that links classes are ordered as expected.
        list = doc('.download-platform-list li')
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_win64')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux64')
        eq_(pq(list[3]).attr('class'), 'os_win')
        eq_(pq(list[4]).attr('class'), 'os_linux')

        links = doc('.download-platform-list a')

        # Check desktop links have the correct version
        self.check_desktop_links(links)

        for link in links:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['en-US'])

    def test_firefox_desktop_list_aurora(self):
        """
        All aurora download links must be directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox_desktop_list(channel='alpha') }}",
                        {'request': get_request}))

        # Check that links classes are ordered as expected.
        list = doc('.download-platform-list li')
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_win64')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux64')
        eq_(pq(list[3]).attr('class'), 'os_win')
        eq_(pq(list[4]).attr('class'), 'os_linux')

        links = doc('.download-platform-list a')

        for link in links:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['en-US'])

    def test_firefox_desktop_list_nightly(self):
        """
        All nightly download links must be directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox_desktop_list(channel='nightly') }}",
                        {'request': get_request}))

        # Check that links classes are ordered as expected.
        list = doc('.download-platform-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux64')
        eq_(pq(list[3]).attr('class'), 'os_linux')

        links = doc('.download-platform-list a')

        for link in links:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['en-US'])


class TestFirefoxURL(TestCase):
    rf = RequestFactory()

    def _render(self, platform, page, channel=None):
        req = self.rf.get('/')
        if channel:
            tmpl = "{{ firefox_url('%s', '%s', '%s') }}" % (platform, page, channel)
        else:
            tmpl = "{{ firefox_url('%s', '%s') }}" % (platform, page)
        return render(tmpl, {'request': req})

    def test_firefox_all(self):
        """Should return a reversed path for the Firefox download page"""
        ok_(self._render('desktop', 'all').endswith('/firefox/all/'))
        ok_(self._render('desktop', 'all', 'release').endswith('/firefox/all/'))
        ok_(self._render('desktop', 'all', 'beta').endswith('/firefox/beta/all/'))
        ok_(self._render('desktop', 'all', 'alpha').endswith('/firefox/developer/all/'))
        ok_(self._render('desktop', 'all', 'esr').endswith('/firefox/organizations/all/'))
        ok_(self._render('desktop', 'all',
                         'organizations').endswith('/firefox/organizations/all/'))

    def test_firefox_sysreq(self):
        """Should return a reversed path for the Firefox sysreq page"""
        ok_(self._render('desktop', 'sysreq').endswith('/firefox/system-requirements/'))
        ok_(self._render('desktop', 'sysreq',
                         'release').endswith('/firefox/system-requirements/'))
        ok_(self._render('desktop', 'sysreq',
                         'beta').endswith('/firefox/beta/system-requirements/'))
        ok_(self._render('desktop', 'sysreq',
                         'alpha').endswith('/firefox/developer/system-requirements/'))
        ok_(self._render('desktop', 'sysreq',
                         'esr').endswith('/firefox/organizations/system-requirements/'))
        ok_(self._render('desktop', 'sysreq',
                         'organizations').endswith('/firefox/organizations/system-requirements/'))

    def test_desktop_notes(self):
        """Should return a reversed path for the desktop notes page"""
        ok_(self._render('desktop', 'notes').endswith('/firefox/notes/'))
        ok_(self._render('desktop', 'notes', 'release').endswith('/firefox/notes/'))
        ok_(self._render('desktop', 'notes', 'beta').endswith('/firefox/beta/notes/'))
        ok_(self._render('desktop', 'notes', 'alpha').endswith('/firefox/developer/notes/'))
        ok_(self._render('desktop', 'notes', 'esr').endswith('/firefox/organizations/notes/'))
        ok_(self._render('desktop', 'notes',
                         'organizations').endswith('/firefox/organizations/notes/'))

    def test_android_notes(self):
        """Should return a reversed path for the Android notes page"""
        ok_(self._render('android', 'notes').endswith('/firefox/android/notes/'))
        ok_(self._render('android', 'notes', 'release').endswith('/firefox/android/notes/'))
        ok_(self._render('android', 'notes', 'beta').endswith('/firefox/android/beta/notes/'))
        ok_(self._render('android', 'notes', 'alpha').endswith('/firefox/android/aurora/notes/'))
