# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.core.cache import caches
from django.http import Http404
from django.test.client import RequestFactory
from django.test.utils import override_settings

from bedrock.base.urlresolvers import reverse
from mock import patch, Mock
from nose.tools import eq_
from pathlib import Path
from pyquery import PyQuery as pq
from rna.models import Release

from bedrock.firefox.firefox_details import FirefoxDesktop
from bedrock.mozorg.tests import TestCase
from bedrock.releasenotes import views
from bedrock.thunderbird.details import ThunderbirdDesktop


DATA_PATH = str(Path(__file__).parent / 'data')
firefox_desktop = FirefoxDesktop(json_dir=DATA_PATH)
thunderbird_desktop = ThunderbirdDesktop(json_dir=DATA_PATH)


class TestRNAViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        self.render_patch = patch('bedrock.releasenotes.views.l10n_utils.render')
        self.mock_render = self.render_patch.start()
        self.mock_render.return_value.has_header.return_value = False

    def tearDown(self):
        self.render_patch.stop()

    @property
    def last_ctx(self):
        """
        Convenient way to access the context of the last rendered
        response.
        """
        return self.mock_render.call_args[0][2]

    @patch('bedrock.releasenotes.views.get_object_or_404')
    @patch('bedrock.releasenotes.views.Q')
    def test_get_release_or_404(self, Q, get_object_or_404):
        eq_(views.get_release_or_404('version', 'product'),
            get_object_or_404.return_value)
        get_object_or_404.assert_called_with(
            Release, Q.return_value, version='version')
        Q.assert_called_once_with(product='product')

    @patch('bedrock.releasenotes.views.get_object_or_404')
    @patch('bedrock.releasenotes.views.Q')
    def test_get_release_or_404_esr(self, Q, get_object_or_404):
        eq_(views.get_release_or_404('24.5.0', 'Firefox'),
            get_object_or_404.return_value)
        Q.assert_any_call(product='Firefox')
        Q.assert_any_call(product='Firefox Extended Support Release')

    @patch('bedrock.releasenotes.views.get_object_or_404')
    @patch('bedrock.releasenotes.views.Q')
    def test_get_release_or_404_endswith_esr(self, Q, get_object_or_404):
        eq_(views.get_release_or_404('45.0esr', 'Firefox'),
            get_object_or_404.return_value)
        Q.assert_any_call(product='Firefox')
        Q.assert_any_call(product='Firefox Extended Support Release')

    @override_settings(DEV=False)
    @patch('bedrock.releasenotes.views.release_notes_template')
    @patch('bedrock.releasenotes.views.get_release_or_404')
    @patch('bedrock.releasenotes.views.equivalent_release_url')
    def test_release_notes(self, mock_equiv_rel_url, get_release_or_404,
                           mock_release_notes_template):
        """
        Should use release returned from get_release_or_404 with the
        correct params and pass the correct context variables and
        template to l10n_utils.render.
        """
        mock_release = get_release_or_404.return_value
        mock_release.major_version.return_value = '34'
        mock_release.notes.return_value = ([Release(id=1), Release(id=2)],
                                           [Release(id=3), Release(id=4)])

        views.release_notes(self.request, '27.0')
        get_release_or_404.assert_called_with('27.0', 'Firefox')
        mock_release.notes.assert_called_with(public_only=True)
        eq_(self.last_ctx['version'], '27.0')
        eq_(self.last_ctx['release'], mock_release)
        eq_(self.last_ctx['new_features'], [Release(id=1), Release(id=2)])
        eq_(self.last_ctx['known_issues'], [Release(id=3), Release(id=4)])
        eq_(self.mock_render.call_args[0][1],
            mock_release_notes_template.return_value)
        mock_equiv_rel_url.assert_called_with(mock_release)
        mock_release_notes_template.assert_called_with(
            mock_release.channel, 'Firefox', 34)

    @patch('bedrock.releasenotes.views.get_release_or_404')
    @patch('bedrock.releasenotes.views.releasenotes_url')
    def test_release_notes_beta_redirect(self, releasenotes_url,
                                         get_release_or_404):
        """
        Should redirect to url for beta release
        """
        get_release_or_404.side_effect = [Http404, 'mock release']
        releasenotes_url.return_value = '/firefox/27.0beta/releasenotes/'
        response = views.release_notes(self.request, '27.0')
        eq_(response.status_code, 302)
        eq_(response['location'], '/firefox/27.0beta/releasenotes/')
        get_release_or_404.assert_called_with('27.0beta', 'Firefox')
        releasenotes_url.assert_called_with('mock release')

    @patch('bedrock.releasenotes.views.get_release_or_404')
    def test_system_requirements(self, get_release_or_404):
        """
        Should use release returned from get_release_or_404, with a
        default channel of Release and default product of Firefox,
        and pass the version to l10n_utils.render
        """
        views.system_requirements(self.request, '27.0.1')
        get_release_or_404.assert_called_with('27.0.1', 'Firefox')
        eq_(self.last_ctx['release'], get_release_or_404.return_value)
        eq_(self.last_ctx['version'], '27.0.1')
        eq_(self.mock_render.call_args[0][1],
            'firefox/releases/system_requirements.html')

    def test_release_notes_template(self):
        """
        Should return correct template name based on channel
        and product
        """
        eq_(views.release_notes_template('Nightly', 'Firefox'),
            'firefox/releases/nightly-notes.html')
        eq_(views.release_notes_template('Aurora', 'Firefox'),
            'firefox/releases/aurora-notes.html')
        eq_(views.release_notes_template('Aurora', 'Firefox', 35),
            'firefox/releases/dev-browser-notes.html')
        eq_(views.release_notes_template('Aurora', 'Firefox', 34),
            'firefox/releases/aurora-notes.html')
        eq_(views.release_notes_template('Beta', 'Firefox'),
            'firefox/releases/beta-notes.html')
        eq_(views.release_notes_template('Release', 'Firefox'),
            'firefox/releases/release-notes.html')
        eq_(views.release_notes_template('ESR', 'Firefox'),
            'firefox/releases/esr-notes.html')
        eq_(views.release_notes_template('Release', 'Thunderbird'),
            'thunderbird/releases/release-notes.html')
        eq_(views.release_notes_template('Beta', 'Thunderbird'),
            'thunderbird/releases/beta-notes.html')
        eq_(views.release_notes_template('', ''),
            'firefox/releases/release-notes.html')

    @override_settings(DEV=False)
    @patch('bedrock.releasenotes.views.get_object_or_404')
    def test_non_public_release(self, get_object_or_404):
        """
        Should raise 404 if not release.is_public and not settings.DEV
        """
        get_object_or_404.return_value = Release(is_public=False)
        with self.assertRaises(Http404):
            views.get_release_or_404('42', 'Firefox')

    @patch('bedrock.releasenotes.views.releasenotes_url')
    def test_no_equivalent_release_url(self, mock_releasenotes_url):
        """
        Should return None without calling releasenotes_url
        """
        release = Mock()
        release.equivalent_android_release.return_value = None
        release.equivalent_desktop_release.return_value = None
        eq_(views.equivalent_release_url(release), None)
        eq_(mock_releasenotes_url.called, 0)

    @patch('bedrock.releasenotes.views.releasenotes_url')
    def test_android_equivalent_release_url(self, mock_releasenotes_url):
        """
        Should return the url for the equivalent android release
        """
        release = Mock()
        eq_(views.equivalent_release_url(release),
            mock_releasenotes_url.return_value)
        mock_releasenotes_url.assert_called_with(
            release.equivalent_android_release.return_value)

    @patch('bedrock.releasenotes.views.releasenotes_url')
    def test_desktop_equivalent_release_url(self, mock_releasenotes_url):
        """
        Should return the url for the equivalent desktop release
        """
        release = Mock()
        release.equivalent_android_release.return_value = None
        eq_(views.equivalent_release_url(release),
            mock_releasenotes_url.return_value)
        mock_releasenotes_url.assert_called_with(
            release.equivalent_desktop_release.return_value)

    @patch('bedrock.releasenotes.views.android_builds')
    def test_get_download_url_android(self, mock_android_builds):
        """
        Shoud return the download link for the release.channel from
        android_builds
        """
        mock_android_builds.return_value = [{'download_link': '/download'}]
        release = Mock(product='Firefox for Android')
        link = views.get_download_url(release)
        eq_(link, '/download')
        mock_android_builds.assert_called_with(release.channel)

    def test_get_download_url_thunderbird(self):
        release = Mock(product='Thunderbird')
        link = views.get_download_url(release)
        eq_(link, '/en-US/thunderbird/')

    def test_get_download_url_thunderbird_beta(self):
        release = Mock(product='Thunderbird', channel='Beta')
        link = views.get_download_url(release)
        eq_(link, '/en-US/thunderbird/channel/')

    def test_check_url(self):
        eq_(views.check_url('Firefox for Android', '42.0'),
            'https://support.mozilla.org/kb/will-firefox-work-my-mobile-device')
        eq_(views.check_url('Firefox for iOS', '1.4'),
            '/en-US/firefox/ios/1.4/system-requirements/')
        eq_(views.check_url('Firefox', '42.0'),
            '/en-US/firefox/42.0/system-requirements/')


class TestReleaseNotesIndex(TestCase):
    pd_cache = caches['product-details']

    def setUp(self):
        self.pd_cache.clear()

    @patch('bedrock.releasenotes.views.l10n_utils.render')
    @patch('bedrock.releasenotes.views.firefox_desktop', firefox_desktop)
    def test_relnotes_index_firefox(self, render_mock):
        with self.activate('en-US'):
            self.client.get(reverse('firefox.releases.index'))
        releases = render_mock.call_args[0][2]['releases']
        eq_(len(releases), len(firefox_desktop.firefox_history_major_releases))
        eq_(releases[0][0], 36.0)
        eq_(releases[0][1]['major'], '36.0')
        eq_(releases[0][1]['minor'], [])
        eq_(releases[3][0], 33.1)
        eq_(releases[3][1]['major'], '33.1')
        eq_(releases[3][1]['minor'], ['33.1.1'])
        eq_(releases[4][0], 33.0)
        eq_(releases[4][1]['major'], '33.0')
        eq_(releases[4][1]['minor'], ['33.0.1', '33.0.2', '33.0.3'])
        eq_(releases[6][0], 31.0)
        eq_(releases[6][1]['major'], '31.0')
        eq_(releases[6][1]['minor'],
            ['31.1.0', '31.1.1', '31.2.0', '31.3.0', '31.4.0', '31.5.0'])

    @patch('bedrock.releasenotes.views.thunderbird_desktop', thunderbird_desktop)
    def test_relnotes_index_thunderbird(self):
        with self.activate('en-US'):
            response = self.client.get(reverse('thunderbird.releases.index'))
        doc = pq(response.content)
        eq_(len(doc('a[href="0.1.html"]')), 1)
        eq_(len(doc('a[href="1.5.0.2.html"]')), 1)
        eq_(len(doc('a[href="../2.0.0.0/releasenotes/"]')), 1)
        eq_(len(doc('a[href="../3.0.1/releasenotes/"]')), 1)


class TestNotesRedirects(TestCase):
    def _test(self, url_from, url_to):
        with self.activate('en-US'):
            url = '/en-US' + url_from
        response = self.client.get(url)
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/en-US' + url_to)

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='22.0'))
    def test_desktop_release_version(self):
        self._test('/firefox/notes/',
                   '/firefox/22.0/releasenotes/')
        self._test('/firefox/latest/releasenotes/',
                   '/firefox/22.0/releasenotes/')

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='23.0b1'))
    def test_desktop_beta_version(self):
        self._test('/firefox/beta/notes/',
                   '/firefox/23.0beta/releasenotes/')

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='24.0a2'))
    def test_desktop_developer_version(self):
        self._test('/firefox/developer/notes/',
                   '/firefox/24.0a2/auroranotes/')

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='24.2.0esr'))
    def test_desktop_esr_version(self):
        self._test('/firefox/organizations/notes/',
                   '/firefox/24.2.0/releasenotes/')

    @patch('bedrock.releasenotes.views.firefox_android.latest_version',
           Mock(return_value='22.0'))
    def test_android_release_version(self):
        self._test('/firefox/android/notes/',
                   '/firefox/android/22.0/releasenotes/')

    @patch('bedrock.releasenotes.views.firefox_android.latest_version',
           Mock(return_value='23.0b1'))
    def test_android_beta_version(self):
        self._test('/firefox/android/beta/notes/',
                   '/firefox/android/23.0beta/releasenotes/')

    @patch('bedrock.releasenotes.views.firefox_android.latest_version',
           Mock(return_value='24.0a2'))
    def test_android_aurora_version(self):
        self._test('/firefox/android/aurora/notes/',
                   '/firefox/android/24.0a2/auroranotes/')

    @patch('bedrock.releasenotes.views.firefox_ios.latest_version',
           Mock(return_value='1.4'))
    def test_ios_release_version(self):
        self._test('/firefox/ios/notes/',
                   '/firefox/ios/1.4/releasenotes/')

    @patch('bedrock.releasenotes.views.thunderbird_desktop.latest_version',
           Mock(return_value='22.0'))
    def test_thunderbird_release_version(self):
        self._test('/thunderbird/notes/',
                   '/thunderbird/22.0/releasenotes/')
        self._test('/thunderbird/latest/releasenotes/',
                   '/thunderbird/22.0/releasenotes/')

    @patch('bedrock.releasenotes.views.thunderbird_desktop.latest_version',
           Mock(return_value='41.0b1'))
    def test_thunderbird_beta_version(self):
        self._test('/thunderbird/beta/notes/',
                   '/thunderbird/41.0beta/releasenotes/')


class TestSysreqRedirect(TestCase):
    def _test(self, url_from, url_to):
        with self.activate('en-US'):
            url = '/en-US' + url_from
        response = self.client.get(url)
        eq_(response.status_code, 302)
        eq_(response['Location'], 'http://testserver/en-US' + url_to)

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='22.0'))
    def test_desktop_release_version(self):
        self._test('/firefox/system-requirements/',
                   '/firefox/22.0/system-requirements/')

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='23.0b1'))
    def test_desktop_beta_version(self):
        self._test('/firefox/beta/system-requirements/',
                   '/firefox/23.0beta/system-requirements/')

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='24.0a2'))
    def test_desktop_developer_version(self):
        self._test('/firefox/developer/system-requirements/',
                   '/firefox/24.0a2/system-requirements/')

    @patch('bedrock.releasenotes.views.firefox_desktop.latest_version',
           Mock(return_value='24.2.0esr'))
    def test_desktop_esr_version(self):
        self._test('/firefox/organizations/system-requirements/',
                   '/firefox/24.0/system-requirements/')

    @patch('bedrock.releasenotes.views.thunderbird_desktop.latest_version',
           Mock(return_value='22.0'))
    def test_thunderbird_release_version(self):
        self._test('/thunderbird/system-requirements/',
                   '/thunderbird/22.0/system-requirements/')
        self._test('/thunderbird/latest/system-requirements/',
                   '/thunderbird/22.0/system-requirements/')

    @patch('bedrock.releasenotes.views.thunderbird_desktop.latest_version',
           Mock(return_value='41.0b1'))
    def test_thunderbird_beta_version(self):
        self._test('/thunderbird/beta/system-requirements/',
                   '/thunderbird/41.0beta/system-requirements/')
