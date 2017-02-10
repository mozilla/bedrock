from urlparse import parse_qs, urlparse

from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings

from django_jinja.backend import Jinja2
from mock import patch, Mock
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq

from product_details import product_details
from bedrock.mozorg.tests import TestCase
from bedrock.firefox.templatetags import helpers
from bedrock.firefox.firefox_details import firefox_android

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
            'firefox-latest',
            'firefox-beta-stub',
            'firefox-beta-latest',
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
        eq_(pq(links[5]).attr('href'), settings.APPLE_APPSTORE_FIREFOX_LINK
                                            .replace('/{country}/', '/'))

    @patch('bedrock.firefox.firefox_details.switch', Mock(return_value=False))
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

        # Check that the first 6 links are direct.
        links = doc('.download-list a')

        # The first link should be sha-1 bouncer.
        first_link = pq(links[0])
        first_href = first_link.attr('href')
        ok_(first_href.startswith('https://download-sha1.allizom.org'))
        self.assertListEqual(parse_qs(urlparse(first_href).query)['lang'], ['fr'])
        ok_(first_link.attr('data-direct-link') is None)

        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['fr'])
            # direct links should not have the data attr.
            ok_(link.attr('data-direct-link') is None)

    @patch('bedrock.firefox.firefox_details.switch', Mock(return_value=False))
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

        # The first 6 links should be for desktop.
        links = doc('.download-list a')

        # The first link should be sha-1 bouncer.
        first_link = pq(links[0])
        ok_(first_link.attr('data-direct-link')
            .startswith('https://download-sha1.allizom.org'))

        for link in links[1:5]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))

        # The seventh link is mobile and should not have the attr
        ok_(pq(links[6]).attr('data-direct-link') is None)

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
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_osx')
        eq_(pq(list[3]).attr('class'), 'os_linux')
        eq_(pq(list[4]).attr('class'), 'os_linux64')
        ok_('stub' in pq(pq(list[1]).find('a')[0]).attr('href'))

    def test_aurora_desktop(self):
        """The Aurora channel should have Windows 64 build"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 6)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_win64')
        eq_(pq(list[3]).attr('class'), 'os_osx')
        eq_(pq(list[4]).attr('class'), 'os_linux')
        eq_(pq(list[5]).attr('class'), 'os_linux64')

    def test_beta_desktop(self):
        """The Beta channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('beta', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 6)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_win64')
        eq_(pq(list[3]).attr('class'), 'os_osx')
        eq_(pq(list[4]).attr('class'), 'os_linux')
        eq_(pq(list[5]).attr('class'), 'os_linux64')

    def test_firefox_desktop(self):
        """The Release channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 6)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_win64')
        eq_(pq(list[3]).attr('class'), 'os_osx')
        eq_(pq(list[4]).attr('class'), 'os_linux')
        eq_(pq(list[5]).attr('class'), 'os_linux64')

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(nightly_version='48.0a2')))
    def test_latest_nightly_android(self):
        """Android Gingerbread (2.3) is no longer supported as of Firefox 48"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('nightly', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 2)
        eq_(pq(list[0]).attr('class'), 'os_android armv7up api-15')
        eq_(pq(list[1]).attr('class'), 'os_android x86')

        links = doc('.download-list li a')
        eq_(links.length, 2)
        ok_(pq(links[0]).attr('href').startswith('https://archive.mozilla.org'))
        ok_(pq(links[1]).attr('href').startswith('https://archive.mozilla.org'))

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(nightly_version='47.0a2')))
    def test_legacy_nightly_android(self):
        """Android Gingerbread (2.3) is supported as of Firefox 47"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('nightly', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 3)
        eq_(pq(list[0]).attr('class'), 'os_android armv7up api-9')
        eq_(pq(list[1]).attr('class'), 'os_android armv7up api-15')
        eq_(pq(list[2]).attr('class'), 'os_android x86')

        links = doc('.download-list li a')
        eq_(links.length, 3)
        ok_(pq(links[0]).attr('href').startswith('https://archive.mozilla.org'))
        ok_(pq(links[1]).attr('href').startswith('https://archive.mozilla.org'))
        ok_(pq(links[2]).attr('href').startswith('https://archive.mozilla.org'))

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(alpha_version='48.0a2')))
    def test_latest_aurora_android(self):
        """Android Gingerbread (2.3) is no longer supported as of Firefox 48"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('alpha', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        links = doc('.download-list li a')
        eq_(links.length, 1)
        ok_(pq(links[0]).attr('href').startswith('https://play.google.com'))

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    @patch.object(firefox_android._storage, 'data',
                  Mock(return_value=dict(alpha_version='47.0a2')))
    def test_legacy_aurora_android(self):
        """Android Gingerbread (2.3) is supported as of Firefox 47"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('alpha', platform='android') }}",
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
            'firefox-latest',
            'firefox-beta-stub',
            'firefox-beta-latest',
        ]

        for link in links:
            url = pq(link).attr('href')
            ok_(any(key in url for key in keys))

    @patch('bedrock.firefox.firefox_details.switch', Mock(return_value=False))
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
        eq_(list.length, 6)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_win64')
        eq_(pq(list[3]).attr('class'), 'os_osx')
        eq_(pq(list[4]).attr('class'), 'os_linux')
        eq_(pq(list[5]).attr('class'), 'os_linux64')

        links = doc('.download-platform-list a')

        # Check desktop links have the correct version
        self.check_desktop_links(links)

        # The first link should be sha-1 bouncer.
        first_link = pq(links[0])
        first_href = first_link.attr('href')
        ok_(first_href.startswith('https://download-sha1.allizom.org'))
        self.assertListEqual(parse_qs(urlparse(first_href).query)['lang'], ['en-US'])

        # All other links should be to regular bouncer.
        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['en-US'])

    @patch('bedrock.firefox.firefox_details.switch', Mock(return_value=False))
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
        eq_(list.length, 6)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_win64')
        eq_(pq(list[3]).attr('class'), 'os_osx')
        eq_(pq(list[4]).attr('class'), 'os_linux')
        eq_(pq(list[5]).attr('class'), 'os_linux64')

        links = doc('.download-platform-list a')

        # The first link should be sha-1 bouncer.
        first_link = pq(links[0])
        first_href = first_link.attr('href')
        ok_(first_href.startswith('https://download-sha1.allizom.org'))
        self.assertListEqual(parse_qs(urlparse(first_href).query)['lang'], ['en-US'])

        # All other links should be to regular bouncer.
        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            ok_(href.startswith('https://download.mozilla.org'))
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['en-US'])

    @patch('bedrock.firefox.firefox_details.switch', Mock(return_value=False))
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
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_winsha1')
        eq_(pq(list[1]).attr('class'), 'os_win')
        eq_(pq(list[2]).attr('class'), 'os_osx')
        eq_(pq(list[3]).attr('class'), 'os_linux')
        eq_(pq(list[4]).attr('class'), 'os_linux64')

        links = doc('.download-platform-list a')

        # The first link should be sha-1 bouncer.
        first_link = pq(links[0])
        first_href = first_link.attr('href')
        ok_(first_href.startswith('https://download-sha1.allizom.org'))
        self.assertListEqual(parse_qs(urlparse(first_href).query)['lang'], ['en-US'])

        # All other links should be to regular bouncer.
        for link in links[1:5]:
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


@override_settings(FIREFOX_OS_FEED_LOCALES=['xx'])
@patch('bedrock.firefox.templatetags.helpers.cache')
@patch('bedrock.firefox.templatetags.helpers.FirefoxOSFeedLink')
class FirefoxOSFeedLinksTest(TestCase):
    def test_no_feed_for_locale(self, FirefoxOSFeedLink, cache):
        """
        Should return None without checking cache or db.
        """
        eq_(helpers.firefox_os_feed_links('yy'), None)
        assert_false(cache.get.called)
        assert_false(FirefoxOSFeedLink.objects.filter.called)

    def test_force_cache_refresh(self, FirefoxOSFeedLink, cache):
        """
        Should force cache update of first 10 values without cache.get()
        """

        (FirefoxOSFeedLink.objects.filter.return_value.order_by.return_value
         .values_list.return_value) = range(20)
        eq_(helpers.firefox_os_feed_links('xx', force_cache_refresh=True),
            range(10))
        assert_false(cache.get.called)
        FirefoxOSFeedLink.objects.filter.assert_called_with(locale='xx')
        cache.set.assert_called_with('firefox-os-feed-links-xx', range(10))

    def test_cache_miss(self, FirefoxOSFeedLink, cache):
        """
        Should update cache with first 10 items from db query
        """
        cache.get.return_value = None
        (FirefoxOSFeedLink.objects.filter.return_value.order_by.return_value
         .values_list.return_value) = range(20)
        eq_(helpers.firefox_os_feed_links('xx'), range(10))
        cache.get.assert_called_with('firefox-os-feed-links-xx')
        FirefoxOSFeedLink.objects.filter.assert_called_with(locale='xx')
        cache.set.assert_called_with('firefox-os-feed-links-xx', range(10))

    def test_hyphenated_cached(self, FirefoxOSFeedLink, cache):
        """
        Should construct cache key with only first part of hyphenated locale.
        """
        eq_(helpers.firefox_os_feed_links('xx-xx'), cache.get.return_value)
        cache.get.assert_called_with('firefox-os-feed-links-xx')
        assert_false(FirefoxOSFeedLink.objects.filter.called)


class FirefoxOSBlogLinkTest(TestCase):
    def test_correct_link_returned_for_es(self):
        """
        Should return the corect link for the es-ES locale
        """
        blog_link_es = 'https://blog.mozilla.org/press-es/category/firefox-os/'

        eq_(helpers.firefox_os_blog_link('es-ES'), blog_link_es)

    def test_correct_link_returned_for_locale_prefix(self):
        """
        Should return the latam link for the es-mx and es-ar locale
        """
        blog_link_latam = 'https://blog.mozilla.org/press-latam/category/firefox-os/'

        eq_(helpers.firefox_os_blog_link('es-mx'), blog_link_latam)
        eq_(helpers.firefox_os_blog_link('es-ar'), blog_link_latam)

    def test_none_returned(self):
        """
        Should return None as the locale will not be found
        """
        eq_(helpers.firefox_os_blog_link('esmx'), None)


class TestFirefoxFooterLinks(TestCase):
    def test_show_all_links(self):
        """Should show all links by default"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links() }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 3)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_android')
        eq_(pq(list[1]).attr('class'), 'fx-footer-links os_ios')
        eq_(pq(list[2]).attr('class'), 'fx-footer-links os_desktop os_other')

    def test_ios_links(self):
        """Should show iOS links only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(platform='ios') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_ios')

        links = doc('.fx-footer-links a')
        eq_(links.length, 2)
        eq_(pq(links[0]).attr('href'),
            'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device')
        ok_(pq(links[1]).attr('href').endswith('/firefox/ios/notes/'))

    def test_android_links(self):
        """Should show Android links only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(platform='android') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_android')

        links = doc('.fx-footer-links a')
        eq_(links.length, 3)
        eq_(pq(links[0]).attr('href'),
            'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device')
        ok_(pq(links[1]).attr('href').endswith('/firefox/android/all/'))
        ok_(pq(links[2]).attr('href').endswith('/firefox/android/notes/'))

    def test_android_beta_links(self):
        """Should show Android Beta links only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(platform='android', channel='beta') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_android')

        links = doc('.fx-footer-links a')
        eq_(links.length, 3)
        eq_(pq(links[0]).attr('href'),
            'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device')
        ok_(pq(links[1]).attr('href').endswith('/firefox/android/beta/all/'))
        ok_(pq(links[2]).attr('href').endswith('/firefox/android/beta/notes/'))

    def test_android_aurora_links(self):
        """Should show Android Aurora links only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(platform='android', channel='alpha') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_android')

        # Note: not testing Android Aurora links as additional build links are
        # dynamically included from product details.

    def test_desktop_links(self):
        """Should show Desktop links only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_desktop os_other')

        links = doc('.fx-footer-links a')
        eq_(links.length, 2)
        ok_(pq(links[0]).attr('href').endswith('/firefox/all/'))
        ok_(pq(links[1]).attr('href').endswith('/firefox/notes/'))

    def test_desktop_beta_links(self):
        """Should show Desktop Betalinks only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(channel='beta', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_desktop os_other')

        links = doc('.fx-footer-links a')
        eq_(links.length, 2)
        ok_(pq(links[0]).attr('href').endswith('/firefox/beta/all/'))
        ok_(pq(links[1]).attr('href').endswith('/firefox/beta/notes/'))

    def test_desktop_developer_links(self):
        """Should show Desktop Developer links only"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ firefox_footer_links(channel='alpha', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.fx-footer-links')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'fx-footer-links os_desktop os_other')

        links = doc('.fx-footer-links a')
        eq_(links.length, 2)
        ok_(pq(links[0]).attr('href').endswith('/firefox/developer/all/'))
        ok_(pq(links[1]).attr('href').endswith('/firefox/developer/notes/'))
