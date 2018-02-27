# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from itertools import chain

from django.core.cache import caches
from django.test.utils import override_settings

from mock import call, patch
from pathlib2 import Path

from bedrock.mozorg.tests import TestCase
from bedrock.releasenotes import models


RELEASES_PATH = str(Path(__file__).parent)
release_cache = caches['release-notes']


@patch('bedrock.releasenotes.models.reverse')
class TestReleaseNotesURL(TestCase):
    def test_aurora_android_releasenotes_url(self, mock_reverse):
        """
        Should return the results of reverse with the correct args
        """
        release = models.ProductRelease(channel='Aurora', version='42.0a2', product='Firefox for Android')
        assert release.get_absolute_url() == mock_reverse.return_value
        mock_reverse.assert_called_with('firefox.android.releasenotes', args=['42.0a2', 'aurora'])

    def test_desktop_releasenotes_url(self, mock_reverse):
        """
        Should return the results of reverse with the correct args
        """
        release = models.ProductRelease(version='42.0', product='Firefox')
        assert release.get_absolute_url() == mock_reverse.return_value
        mock_reverse.assert_called_with('firefox.desktop.releasenotes', args=['42.0', 'release'])


@override_settings(RELEASE_NOTES_PATH=RELEASES_PATH, DEV=False)
class TestReleaseModel(TestCase):
    def setUp(self):
        models.ProductRelease.objects.refresh()
        release_cache.clear()

    def test_release_major_version(self):
        rel = models.get_release('firefox', '57.0a1')
        assert rel.major_version == '57'

    def test_get_bug_search_url(self):
        rel = models.get_release('firefox', '57.0a1')
        assert '=Firefox%2057&' in rel.get_bug_search_url()
        rel.bug_search_url = 'custom url'
        assert 'custom url' == rel.get_bug_search_url()

    def test_equivalent_release_for_product(self):
        """Based on the test files the equivalent release for 56 should be 56.0.2"""
        rel = models.get_release('firefox', '56.0', 'release')
        android = rel.equivalent_release_for_product('Firefox for Android')
        assert android.version == '56.0.2'
        assert android.product == 'Firefox for Android'

    def test_equivalent_release_for_product_none_match(self):
        rel = models.get_release('firefox', '45.0esr')
        android = rel.equivalent_release_for_product('Firefox for Android')
        assert android is None

    def test_note_fixed_in_release(self):
        rel = models.get_release('firefox', '55.0a1')
        note = rel.notes[11]
        with self.activate('en-US'):
            assert note.fixed_in_release.get_absolute_url() == '/en-US/firefox/55.0a1/releasenotes/'

    def test_field_processors(self):
        rel = models.get_release('firefox', '57.0a1')
        # datetime conversion
        assert rel.created.year == 2017
        # datetime conversion
        assert rel.modified.year == 2017
        # date conversion
        assert rel.release_date.year == 2017
        # markdown
        assert rel.system_requirements.startswith('<h2 id="windows">Windows</h2>')
        # version
        assert rel.version_obj.major == 57

        # notes
        note = rel.notes[0]
        # datetime conversion
        assert note.created.year == 2017
        # datetime conversion
        assert note.modified.year == 2017
        # markdown
        assert note.note.startswith('<p>Firefox Nightly')
        assert note.id == 787203

    @override_settings(DEV=False)
    def test_is_public_query(self):
        """Should not return the release value when DEV is false.

        Should also only include public notes."""
        assert models.get_release('firefox for android', '56.0.3') is None
        rel = models.get_release('firefox', '57.0a1')
        assert len(rel.notes) == 4

    @override_settings(DEV=True)
    def test_is_public_field_processor_dev_true(self):
        """Should always be true when DEV is true."""
        models.get_release('firefox for android', '56.0.3')
        rel = models.get_release('firefox', '57.0a1')
        assert len(rel.notes) == 6


@patch.object(models.ProductRelease, 'objects')
class TestGetRelease(TestCase):
    def setUp(self):
        release_cache.clear()

    def test_get_release(self, manager_mock):
        manager_mock.product().get.return_value = 'dude is released'
        assert models.get_release('Firefox', '57.0') == 'dude is released'
        manager_mock.product.assert_called_with('Firefox', models.ProductRelease.CHANNELS[0], '57.0', False)

    def test_get_release_esr(self, manager_mock):
        manager_mock.product().get.return_value = 'dude is released'
        assert models.get_release('Firefox Extended Support Release', '51.0') == 'dude is released'
        manager_mock.product.assert_called_with('Firefox Extended Support Release', 'esr', '51.0', False)

    def test_get_release_none_match(self, manager_mock):
        """Make sure the proper exception is raised if no file matches the query"""
        manager_mock.product().get.side_effect = models.ProductRelease.DoesNotExist
        assert models.get_release('Firefox', '57.0') is None

        expected_calls = chain.from_iterable(
            (call('Firefox', ch, '57.0', False), call().get()) for ch in models.ProductRelease.CHANNELS)
        manager_mock.product.assert_has_calls(expected_calls)


@override_settings(RELEASE_NOTES_PATH=RELEASES_PATH, DEV=False)
class TestGetLatestRelease(TestCase):
    def setUp(self):
        models.ProductRelease.objects.refresh()
        release_cache.clear()

    def test_latest_release(self):
        correct_release = models.get_release('firefox for android', '56.0.2')
        assert models.get_latest_release('firefox for android', 'release') == correct_release

    def test_non_public_release_not_duped(self):
        # refresh again
        models.ProductRelease.objects.refresh()
        release_cache.clear()
        # non public release
        # should NOT raise multiple objects error
        assert models.get_release('firefox for android', '56.0.3', include_drafts=True)
