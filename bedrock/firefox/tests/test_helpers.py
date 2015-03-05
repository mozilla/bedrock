import jingo
from django.conf import settings
from django.test.client import RequestFactory
from django.test.utils import override_settings

from mock import patch
from nose.tools import assert_false, eq_, ok_
from pyquery import PyQuery as pq

from product_details import product_details
from bedrock.mozorg.tests import TestCase
from bedrock.firefox import helpers


def render(s, context=None):
    t = jingo.env.from_string(s)
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

        # Check that last link is Android
        eq_(pq(links[4]).attr('href'), settings.GOOGLE_PLAY_FIREFOX_LINK)

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

        # Check that the first 4 links are direct.
        links = doc('.download-list a')
        for link in links[:4]:
            link = pq(link)
            ok_(link.attr('href')
                .startswith('https://download.mozilla.org'))
            # direct links should not have the data attr.
            ok_(link.attr('data-direct-link') is None)

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

        # The first 4 links should be for desktop.
        links = doc('.download-list a')
        for link in links[:4]:
            ok_(pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))
        # The fourth link is mobile and should not have the attr
        ok_(pq(links[4]).attr('data-direct-link') is None)

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_enabled_locales(self):
        """Check that the stub is not served to locales"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha') }}",
                        {'request': get_request}))

        links = doc('.download-list a')
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=False)
    def test_stub_aurora_installer_disabled_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha') }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    @override_settings(AURORA_STUB_INSTALLER=True)
    def test_stub_aurora_installer_override_locale(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha', "
                        "force_full_installer=True) }}",
                        {'request': get_request}))

        links = doc('.download-list a')[:4]
        for link in links:
            ok_('stub' not in pq(link).attr('href'))

    def test_aurora_desktop(self):
        """The Aurora channel should have Windows 64 build"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 5)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_win64')
        eq_(pq(list[2]).attr('class'), 'os_osx')
        eq_(pq(list[3]).attr('class'), 'os_linux')
        eq_(pq(list[4]).attr('class'), 'os_linux64')

    def test_beta_desktop(self):
        """The Beta channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('beta', platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux')
        eq_(pq(list[3]).attr('class'), 'os_linux64')

    def test_firefox_desktop(self):
        """The Release channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(platform='desktop') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 4)
        eq_(pq(list[0]).attr('class'), 'os_win')
        eq_(pq(list[1]).attr('class'), 'os_osx')
        eq_(pq(list[2]).attr('class'), 'os_linux')
        eq_(pq(list[3]).attr('class'), 'os_linux64')

    def test_aurora_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('alpha', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 3)
        eq_(pq(list[0]).attr('class'), 'os_android armv7 api-9')
        eq_(pq(list[1]).attr('class'), 'os_android armv7 api-11')
        eq_(pq(list[2]).attr('class'), 'os_android x86')

        list = doc('.download-other .arch')
        eq_(list.length, 3)
        eq_(pq(list[0]).attr('class'), 'arch armv7 api-9')
        eq_(pq(list[1]).attr('class'), 'arch armv7 api-11')
        eq_(pq(list[2]).attr('class'), 'arch x86')

    def test_beta_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox('beta', platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_firefox_mobile(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox(platform='android') }}",
                        {'request': get_request}))

        list = doc('.download-list li')
        eq_(list.length, 1)
        eq_(pq(list[0]).attr('class'), 'os_android')

        list = doc('.download-other .arch')
        eq_(list.length, 0)

    def test_check_old_firefox(self):
        """
        Make sure check_old_fx class is only applied if both check_old_fx=True
        and simple=True.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'

        # missing required 'simple=True' param
        doc = pq(render("{{ download_firefox(check_old_fx=True) }}",
                        {'request': get_request}))

        dlbuttons = doc('.download-button')
        eq_(dlbuttons.length, 1)

        # 'download-button-check-old-fx' class should not be present
        dlbtn = pq(dlbuttons[0])
        self.assertFalse(dlbtn('.download-button-check-old-fx'))

        # contains required 'simple=True' param
        doc = pq(render("{{ download_firefox(simple=True, check_old_fx=True) }}",
                        {'request': get_request}))

        dlbuttons = doc('.download-button')
        eq_(dlbuttons.length, 1)

        # 'download-button-check-old-fx' class should be present
        dlbtn = pq(dlbuttons[0])
        self.assertTrue(dlbtn('.download-button-check-old-fx'))


class TestFirefoxURL(TestCase):
    rf = RequestFactory()

    def _render(self, platform, page, channel=None):
        req = self.rf.get('/')
        req.locale = 'en-US'
        if channel:
            tmpl = "{{ firefox_url('%s', '%s', '%s') }}" % (platform, page, channel)
        else:
            tmpl = "{{ firefox_url('%s', '%s') }}" % (platform, page)
        return render(tmpl, {'request': req})

    def test_firefox_all(self):
        """Should return a reversed path for the Firefox download page"""
        eq_(self._render('desktop', 'all'),
            '/en-US/firefox/all/')
        eq_(self._render('desktop', 'all', 'release'),
            '/en-US/firefox/all/')
        eq_(self._render('desktop', 'all', 'beta'),
            '/en-US/firefox/beta/all/')
        eq_(self._render('desktop', 'all', 'alpha'),
            '/en-US/firefox/developer/all/')
        eq_(self._render('desktop', 'all', 'esr'),
            '/en-US/firefox/organizations/all/')
        eq_(self._render('desktop', 'all', 'organizations'),
            '/en-US/firefox/organizations/all/')

    def test_firefox_sysreq(self):
        """Should return a reversed path for the Firefox sysreq page"""
        eq_(self._render('desktop', 'sysreq'),
            '/en-US/firefox/system-requirements/')
        eq_(self._render('desktop', 'sysreq', 'release'),
            '/en-US/firefox/system-requirements/')
        eq_(self._render('desktop', 'sysreq', 'beta'),
            '/en-US/firefox/beta/system-requirements/')
        eq_(self._render('desktop', 'sysreq', 'alpha'),
            '/en-US/firefox/developer/system-requirements/')
        eq_(self._render('desktop', 'sysreq', 'esr'),
            '/en-US/firefox/organizations/system-requirements/')
        eq_(self._render('desktop', 'sysreq', 'organizations'),
            '/en-US/firefox/organizations/system-requirements/')

    def test_firefox_notes(self):
        """Should return a reversed path for the Firefox notes page"""
        eq_(self._render('desktop', 'notes'),
            '/en-US/firefox/notes/')
        eq_(self._render('desktop', 'notes', 'release'),
            '/en-US/firefox/notes/')
        eq_(self._render('desktop', 'notes', 'beta'),
            '/en-US/firefox/beta/notes/')
        eq_(self._render('desktop', 'notes', 'alpha'),
            '/en-US/firefox/developer/notes/')
        eq_(self._render('desktop', 'notes', 'esr'),
            '/en-US/firefox/organizations/notes/')
        eq_(self._render('desktop', 'notes', 'organizations'),
            '/en-US/firefox/organizations/notes/')

    def test_mobile_notes(self):
        """Should return a reversed path for the mobile notes page"""
        eq_(self._render('android', 'notes'),
            '/en-US/mobile/notes/')
        eq_(self._render('android', 'notes', 'release'),
            '/en-US/mobile/notes/')
        eq_(self._render('android', 'notes', 'beta'),
            '/en-US/mobile/beta/notes/')
        eq_(self._render('android', 'notes', 'alpha'),
            '/en-US/mobile/aurora/notes/')


@override_settings(FIREFOX_OS_FEED_LOCALES=['xx'])
@patch('bedrock.firefox.helpers.cache')
@patch('bedrock.firefox.helpers.FirefoxOSFeedLink')
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
