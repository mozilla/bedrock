# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.http import Http404
from django.test.client import RequestFactory
from django.test.utils import override_settings

from mock import patch
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
    def test_release_notes(self, get_object_or_404):
        """
        Should use release returned from get_object_or_404 with the
        correct params and pass the correct context variables and
        template to l10n_utils.render
        """
        mock_release = get_object_or_404.return_value
        mock_release.notes.return_value = ('mock new_features',
                                           'mock known_issues')

        views.release_notes(self.request, '27.0')
        # Should use fixed version for query
        get_object_or_404.assert_called_with(
            Release, version='27.0', product='Firefox')
        # Should use original version for context variable
        eq_(self.last_ctx['version'], '27.0')
        eq_(self.last_ctx['major_version'], '27')
        eq_(self.last_ctx['release'], mock_release)
        eq_(self.last_ctx['new_features'], 'mock new_features')
        eq_(self.last_ctx['known_issues'], 'mock known_issues')
        eq_(self.mock_render.call_args[0][1],
            'firefox/releases/release-notes.html')

    @patch('bedrock.firefox.views.get_object_or_404')
    def test_system_requirements(self, get_object_or_404):
        """
        Should use release returned from get_object_or_404, with a
        default channel of Release and default product of Firefox,
        and pass the version to l10n_utils.render
        """
        views.system_requirements(self.request, '27.0.1')
        get_object_or_404.assert_called_with(
            Release, version='27.0.1', product='Firefox')
        eq_(self.last_ctx['release'], get_object_or_404.return_value)
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

    @patch('bedrock.firefox.views.get_object_or_404')
    def test_firefox_os_manual_template(self, get_object_or_404):
        """
        Should render from pre-RNA template without querying DB
        """
        views.release_notes(self.request, '1.0.1', product='Firefox OS')
        get_object_or_404.assert_never_called()
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
            views.release_notes(self.request, '42')
