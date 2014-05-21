# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.http import Http404
from django.test.client import RequestFactory
from django.test.utils import override_settings

from mock import patch, Mock
from nose.tools import eq_
from rna.models import Release

from bedrock.firefox import views
from bedrock.mozorg.tests import TestCase


class TestRNAViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        self.render_patch = patch('bedrock.firefox.views.l10n_utils.render')
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

    @patch('bedrock.firefox.views.get_object_or_404')
    @patch('bedrock.firefox.views.Q')
    def test_get_release_or_404(self, Q, get_object_or_404):
        eq_(views.get_release_or_404('version', 'product'),
            get_object_or_404.return_value)
        get_object_or_404.assert_called_with(
            Release, Q.return_value, version='version')
        Q.assert_called_with(product='product')

    @patch('bedrock.firefox.views.get_object_or_404')
    @patch('bedrock.firefox.views.Q')
    def test_get_release_or_404_esr(self, Q, get_object_or_404):
        eq_(views.get_release_or_404('24.5.0', 'Firefox'),
            get_object_or_404.return_value)
        Q.assert_any_call(product='Firefox')
        Q.assert_any_call(product='Firefox Extended Support Release')
        Q.__or__.assert_called()

    @override_settings(DEV=True)
    @patch('bedrock.firefox.views.get_release_or_404')
    @patch('bedrock.firefox.views.equivalent_release_url')
    def test_release_notes_dev(self, mock_equiv_rel_url, get_release_or_404):
        """
        Should use release returned from get_release_or_404 with the
        correct params and pass the correct context variables and
        template to l10n_utils.render. Should not filter notes.
        """
        mock_release = get_release_or_404.return_value
        mock_release.notes.return_value = (
            [Release(id=1, is_public=True), Release(id=2, is_public=False)],
            [Release(id=3, is_public=True), Release(id=4, is_public=False)])

        views.release_notes(self.request, '27.0')
        # Should use fixed version for query
        get_release_or_404.assert_called_with('27.0', 'Firefox')
        # Should use original version for context variable
        eq_(self.last_ctx['version'], '27.0')
        eq_(self.last_ctx['release'], mock_release)
        eq_(self.last_ctx['new_features'], [Release(id=1), Release(id=2)])
        eq_(self.last_ctx['known_issues'], [Release(id=3), Release(id=4)])
        eq_(self.mock_render.call_args[0][1],
            'firefox/releases/release-notes.html')
        mock_equiv_rel_url.assert_called_with(mock_release)

    @override_settings(DEV=False)
    @patch('bedrock.firefox.views.get_release_or_404')
    @patch('bedrock.firefox.views.equivalent_release_url')
    def test_release_notes_prod(self, mock_equiv_rel_url, get_release_or_404):
        """
        Should use release returned from get_release_or_404 with the
        correct params and pass the correct context variables and
        template to l10n_utils.render. Should filter notes based on is_public.
        """
        mock_release = get_release_or_404.return_value
        mock_release.notes.return_value = (
            [Release(id=1, is_public=True), Release(id=2, is_public=False)],
            [Release(id=3, is_public=True), Release(id=4, is_public=False)])

        views.release_notes(self.request, '27.0')
        # Should use fixed version for query
        get_release_or_404.assert_called_with('27.0', 'Firefox')
        # Should use original version for context variable
        eq_(self.last_ctx['version'], '27.0')
        eq_(self.last_ctx['release'], mock_release)
        eq_(self.last_ctx['new_features'], [Release(id=1)])
        eq_(self.last_ctx['known_issues'], [Release(id=3)])
        eq_(self.mock_render.call_args[0][1],
            'firefox/releases/release-notes.html')
        mock_equiv_rel_url.assert_called_with(mock_release)

    @patch('bedrock.firefox.views.get_release_or_404')
    @patch('bedrock.firefox.views.releasenotes_url')
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

    @patch('bedrock.firefox.views.get_release_or_404')
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
        eq_(views.release_notes_template('', 'Firefox OS'),
            'firefox/releases/os-notes.html')
        eq_(views.release_notes_template('Nightly', 'Firefox'),
            'firefox/releases/nightly-notes.html')
        eq_(views.release_notes_template('Aurora', 'Firefox'),
            'firefox/releases/aurora-notes.html')
        eq_(views.release_notes_template('Beta', 'Firefox'),
            'firefox/releases/beta-notes.html')
        eq_(views.release_notes_template('Release', 'Firefox'),
            'firefox/releases/release-notes.html')
        eq_(views.release_notes_template('ESR', 'Firefox'),
            'firefox/releases/esr-notes.html')
        eq_(views.release_notes_template('', ''),
            'firefox/releases/release-notes.html')

    @patch('bedrock.firefox.views.get_release_or_404')
    def test_firefox_os_manual_template(self, get_release_or_404):
        """
        Should render from pre-RNA template without querying DB
        """
        views.release_notes(self.request, '1.0.1', product='Firefox OS')
        get_release_or_404.assert_never_called()
        eq_(self.mock_render.call_args[0][1],
            'firefox/os/notes-1.0.1.html')

    @override_settings(DEV=False)
    @patch('bedrock.firefox.views.get_object_or_404')
    def test_non_public_release(self, get_object_or_404):
        """
        Should raise 404 if not release.is_public and not settings.DEV
        """
        get_object_or_404.return_value = Release(is_public=False)
        with self.assertRaises(Http404):
            views.get_release_or_404('42', 'Firefox')

    @patch('bedrock.firefox.views.releasenotes_url')
    def test_no_equivalent_release_url(self, mock_releasenotes_url):
        """
        Should return None without calling releasenotes_url
        """
        release = Mock()
        release.equivalent_android_release.return_value = None
        release.equivalent_desktop_release.return_value = None
        eq_(views.equivalent_release_url(release), None)
        eq_(mock_releasenotes_url.called, 0)

    @patch('bedrock.firefox.views.releasenotes_url')
    def test_android_equivalent_release_url(self, mock_releasenotes_url):
        """
        Should return the url for the equivalent android release
        """
        release = Mock()
        eq_(views.equivalent_release_url(release),
            mock_releasenotes_url.return_value)
        mock_releasenotes_url.assert_called_with(
            release.equivalent_android_release.return_value)

    @patch('bedrock.firefox.views.releasenotes_url')
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
