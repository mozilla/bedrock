from urllib.parse import parse_qs, urlparse

from django.conf import settings
from django.test.client import RequestFactory

from django_jinja.backend import Jinja2
from pyquery import PyQuery as pq

from bedrock.mozorg.tests import TestCase
from lib.l10n_utils.fluent import fluent_l10n

jinja_env = Jinja2.get_default()


def render(s, context=None):
    t = jinja_env.from_string(s)
    return t.render(context or {})


class TestDownloadButtons(TestCase):

    def latest_version(self):
        from product_details import product_details
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def get_l10n(self, locale):
        return fluent_l10n([locale, 'en'], settings.FLUENT_DEFAULT_FILES)

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
            assert any(key in url for key in keys)

    def check_dumb_button(self, doc):
        # Make sure 5 links are present
        links = doc('li a')
        assert links.length == 5

        self.check_desktop_links(links[:4])

        # Check that the rest of the links are Android and iOS
        assert pq(links[4]).attr('href') == settings.GOOGLE_PLAY_FIREFOX_LINK_UTMS
        assert (
            pq(links[5]).attr('href') ==
            settings.APPLE_APPSTORE_FIREFOX_LINK.replace('/{country}/', '/')
        )

    def test_button_force_direct(self):
        """
        If the force_direct parameter is True, all download links must be
        directly to https://download.mozilla.org.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(force_direct=true) }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        # Check that the first 5 links are direct.
        links = doc('.download-list a')

        for link in links[:5]:
            link = pq(link)
            href = link.attr('href')
            assert href.startswith('https://download.mozilla.org')
            self.assertListEqual(parse_qs(urlparse(href).query)['lang'], ['fr'])
            # direct links should not have the data attr.
            assert link.attr('data-direct-link') is None

    def test_button_locale_in_transition(self):
        """
        If the locale_in_transition parameter is True, the link to scene2 should include the locale
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(locale_in_transition=true) }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        links = doc('.download-list a')

        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            assert href == '/fr/firefox/download/thanks/'

        doc = pq(render("{{ download_firefox(locale_in_transition=false) }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        links = doc('.download-list a')

        for link in links[1:5]:
            link = pq(link)
            href = link.attr('href')
            assert href == '/firefox/download/thanks/'

    def test_download_location_attribute(self):
        """
        If the download_location parameter is set, it should be included as a data attribute.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(download_location='primary cta') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        links = doc('.download-list a')

        for link in links:
            link = pq(link)
            assert link.attr('data-download-location') == 'primary cta'

        doc = pq(render("{{ download_firefox() }}", {'request': get_request,
                        'fluent_l10n': self.get_l10n(get_request.locale)}))

        links = doc('.download-list a')

        for link in links[1:5]:
            link = pq(link)
            assert link.attr('data-download-location') is None

    def test_download_nosnippet_attribute(self):
        """
        Unsupported messaging should be well formed <div>'s with data-nosnippet attribute (issue #8739).
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox() }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        unrecognised_message = doc('.unrecognized-download').empty().outerHtml()
        assert unrecognised_message == '<div class="unrecognized-download" data-nosnippet="true"></div>'

    def test_button_has_data_attr_if_not_direct(self):
        """
        If the button points to the thank you page, it should have a
        `data-direct-link` attribute that contains the direct url.
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox() }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        # The first 8 links should be for desktop.
        links = doc('.download-list a')

        for link in links[:8]:
            assert (
                pq(link).attr('data-direct-link')
                .startswith('https://download.mozilla.org'))

        # The ninth link is mobile and should not have the attr
        assert pq(links[8]).attr('data-direct-link') is None

    def test_nightly_desktop(self):
        """
        The Nightly channel should have the Windows universal stub installer
        instead of the Windows 64-bit build
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('nightly', platform='desktop') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        list = doc('.download-list li')
        assert list.length == 7
        assert pq(list[0]).attr('class') == 'os_win'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_win-msi'
        assert pq(list[4]).attr('class') == 'os_osx'
        assert pq(list[5]).attr('class') == 'os_linux64'
        assert pq(list[6]).attr('class') == 'os_linux'
        # stub disabled for now for non-en-US locales
        # bug 1339870
        # assert 'stub' in pq(pq(list[1]).find('a')[0]).attr('href')

    def test_aurora_desktop(self):
        """The Aurora channel should have Windows 64 build"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('alpha', platform='desktop') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        list = doc('.download-list li')
        assert list.length == 8
        assert pq(list[0]).attr('class') == 'os_win64'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_win'
        assert pq(list[4]).attr('class') == 'os_win-msi'
        assert pq(list[5]).attr('class') == 'os_osx'
        assert pq(list[6]).attr('class') == 'os_linux64'
        assert pq(list[7]).attr('class') == 'os_linux'

    def test_beta_desktop(self):
        """The Beta channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox('beta', platform='desktop') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        list = doc('.download-list li')
        assert list.length == 8
        assert pq(list[0]).attr('class') == 'os_win64'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_win'
        assert pq(list[4]).attr('class') == 'os_win-msi'
        assert pq(list[5]).attr('class') == 'os_osx'
        assert pq(list[6]).attr('class') == 'os_linux64'
        assert pq(list[7]).attr('class') == 'os_linux'

    def test_firefox_desktop(self):
        """The Release channel should not have Windows 64 build yet"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'fr'
        doc = pq(render("{{ download_firefox(platform='desktop') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        list = doc('.download-list li')
        assert list.length == 8
        assert pq(list[0]).attr('class') == 'os_win64'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_win'
        assert pq(list[4]).attr('class') == 'os_win-msi'
        assert pq(list[5]).attr('class') == 'os_osx'
        assert pq(list[6]).attr('class') == 'os_linux64'
        assert pq(list[7]).attr('class') == 'os_linux'

    def test_latest_nightly_android(self):
        """The download button should have a Google Play link"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('nightly', platform='android') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n('fr')}))

        list = doc('.download-list li')
        assert list.length == 1
        assert pq(list[0]).attr('class') == 'os_android'

        links = doc('.download-list li a')
        assert links.length == 1
        assert pq(links[0]).attr('href').startswith('https://play.google.com')

        list = doc('.download-other .arch')
        assert list.length == 0

    def test_beta_mobile(self):
        """The download button should have a Google Play link"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox('beta', platform='android') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n('fr')}))

        list = doc('.download-list li')
        assert list.length == 1
        assert pq(list[0]).attr('class') == 'os_android'

        links = doc('.download-list li a')
        assert links.length == 1
        assert pq(links[0]).attr('href').startswith('https://play.google.com')

        list = doc('.download-other .arch')
        assert list.length == 0

    def test_firefox_mobile(self):
        """The download button should have a Google Play link"""
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox(platform='android') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n('fr')}))

        list = doc('.download-list li')
        assert list.length == 1
        assert pq(list[0]).attr('class') == 'os_android'

        links = doc('.download-list li a')
        assert links.length == 1
        assert pq(links[0]).attr('href').startswith('https://play.google.com')

        list = doc('.download-other .arch')
        assert list.length == 0

    def test_ios(self):
        rf = RequestFactory()
        get_request = rf.get('/fake')
        doc = pq(render("{{ download_firefox(platform='ios') }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n('fr')}))

        list = doc('.download-list li')
        assert list.length == 1
        assert pq(list[0]).attr('class') == 'os_ios'


class TestDownloadThanksButton(TestCase):

    def get_l10n(self, locale):
        return fluent_l10n([locale, 'en'], settings.FLUENT_DEFAULT_FILES)

    def test_download_firefox_thanks_button(self):
        """
        Download link should point to /firefox/download/thanks/
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox_thanks() }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        links = doc('.c-button-download-thanks > a')
        assert links.length == 1

        link = pq(links)
        href = link.attr('href')

        assert href == ('/firefox/download/thanks/')
        assert link.attr('id') == 'download-button-thanks'
        assert link.attr('data-link-type') == 'download'

        # Direct attribute for legacy IE browsers should always be win 32bit
        assert link.attr('data-direct-link') == 'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US'

    def test_download_firefox_thanks_attributes(self):
        """
        Download link should support custom attributes
        """
        rf = RequestFactory()
        get_request = rf.get('/fake')
        get_request.locale = 'en-US'
        doc = pq(render("{{ download_firefox_thanks(dom_id='test-download', button_class='test-css-class', "
                        "download_location='primary cta', locale_in_transition=True) }}",
                        {'request': get_request, 'fluent_l10n': self.get_l10n(get_request.locale)}))

        links = doc('.c-button-download-thanks > a')
        assert links.length == 1

        link = pq(links)
        href = link.attr('href')

        assert href == ('/en-US/firefox/download/thanks/')
        assert link.attr('id') == 'test-download'
        assert link.attr('data-download-location') == 'primary cta'
        assert 'test-css-class' in link.attr('class')


class TestDownloadList(TestCase):

    def latest_version(self):
        from product_details import product_details
        return product_details.firefox_versions['LATEST_FIREFOX_VERSION']

    def check_desktop_links(self, links):
        """Desktop links should have the correct firefox version"""
        # valid product strings
        keys = [
            'firefox-%s' % self.latest_version(),
            'firefox-stub',
            'firefox-latest-ssl',
            'firefox-msi-latest-ssl',
            'firefox-beta-stub',
            'firefox-beta-latest-ssl',
        ]

        for link in links:
            url = pq(link).attr('href')
            assert any(key in url for key in keys)

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
        assert list.length == 8
        assert pq(list[0]).attr('class') == 'os_win64'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_osx'
        assert pq(list[4]).attr('class') == 'os_linux64'
        assert pq(list[5]).attr('class') == 'os_linux'
        assert pq(list[6]).attr('class') == 'os_win'
        assert pq(list[7]).attr('class') == 'os_win-msi'

        links = doc('.download-platform-list a')

        # Check desktop links have the correct version
        self.check_desktop_links(links)

        for link in links:
            link = pq(link)
            href = link.attr('href')
            assert href.startswith('https://download.mozilla.org')
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
        assert list.length == 8
        assert pq(list[0]).attr('class') == 'os_win64'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_osx'
        assert pq(list[4]).attr('class') == 'os_linux64'
        assert pq(list[5]).attr('class') == 'os_linux'
        assert pq(list[6]).attr('class') == 'os_win'
        assert pq(list[7]).attr('class') == 'os_win-msi'

        links = doc('.download-platform-list a')

        for link in links:
            link = pq(link)
            href = link.attr('href')
            assert href.startswith('https://download.mozilla.org')
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
        assert list.length == 7
        assert pq(list[0]).attr('class') == 'os_win'
        assert pq(list[1]).attr('class') == 'os_win64-msi'
        assert pq(list[2]).attr('class') == 'os_win64-aarch64'
        assert pq(list[3]).attr('class') == 'os_osx'
        assert pq(list[4]).attr('class') == 'os_linux64'
        assert pq(list[5]).attr('class') == 'os_linux'
        assert pq(list[6]).attr('class') == 'os_win-msi'

        links = doc('.download-platform-list a')

        for link in links:
            link = pq(link)
            href = link.attr('href')
            assert href.startswith('https://download.mozilla.org')
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
        """Should return a reversed path for the Firefox all downloads page"""
        assert self._render('desktop', 'all').endswith('/firefox/all/#product-desktop-release')
        assert self._render('desktop', 'all', 'release').endswith('/firefox/all/#product-desktop-release')
        assert self._render('desktop', 'all', 'beta').endswith('/firefox/all/#product-desktop-beta')
        assert self._render('desktop', 'all', 'alpha').endswith('/firefox/all/#product-desktop-developer')
        assert self._render('desktop', 'all', 'developer').endswith('/firefox/all/#product-desktop-developer')
        assert self._render('desktop', 'all', 'nightly').endswith('/firefox/all/#product-desktop-nightly')
        assert self._render('desktop', 'all', 'esr').endswith('/firefox/all/#product-desktop-esr')
        assert self._render('desktop', 'all', 'organizations').endswith('/firefox/all/#product-desktop-esr')
        assert self._render('android', 'all').endswith('/firefox/all/#product-android-release')
        assert self._render('android', 'all', 'release').endswith('/firefox/all/#product-android-release')
        assert self._render('android', 'all', 'beta').endswith('/firefox/all/#product-android-beta')
        assert self._render('android', 'all', 'nightly').endswith('/firefox/all/#product-android-nightly')

    def test_firefox_sysreq(self):
        """Should return a reversed path for the Firefox sysreq page"""
        assert self._render('desktop', 'sysreq').endswith('/firefox/system-requirements/')
        assert (
            self._render('desktop', 'sysreq', 'release')
            .endswith('/firefox/system-requirements/'))
        assert (
            self._render('desktop', 'sysreq', 'beta')
            .endswith('/firefox/beta/system-requirements/'))
        assert (
            self._render('desktop', 'sysreq', 'alpha')
            .endswith('/firefox/developer/system-requirements/'))
        assert (
            self._render('desktop', 'sysreq', 'esr')
            .endswith('/firefox/organizations/system-requirements/'))
        assert (
            self._render('desktop', 'sysreq', 'organizations')
            .endswith('/firefox/organizations/system-requirements/'))

    def test_desktop_notes(self):
        """Should return a reversed path for the desktop notes page"""
        assert self._render('desktop', 'notes').endswith('/firefox/notes/')
        assert self._render('desktop', 'notes', 'release').endswith('/firefox/notes/')
        assert self._render('desktop', 'notes', 'beta').endswith('/firefox/beta/notes/')
        assert self._render('desktop', 'notes', 'alpha').endswith('/firefox/developer/notes/')
        assert self._render('desktop', 'notes', 'esr').endswith('/firefox/organizations/notes/')
        assert (
            self._render('desktop', 'notes', 'organizations')
            .endswith('/firefox/organizations/notes/'))

    def test_android_notes(self):
        """Should return a reversed path for the Android notes page"""
        assert self._render('android', 'notes').endswith('/firefox/android/notes/')
        assert self._render('android', 'notes', 'release').endswith('/firefox/android/notes/')
        assert self._render('android', 'notes', 'beta').endswith('/firefox/android/beta/notes/')
        assert self._render('android', 'notes', 'alpha').endswith('/firefox/android/aurora/notes/')
