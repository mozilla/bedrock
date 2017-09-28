# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.conf import settings
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
        release = models.Release(dict(
            channel='Aurora', version='42.0a2', product='Firefox for Android'))
        assert release.get_absolute_url() == mock_reverse.return_value
        mock_reverse.assert_called_with('firefox.android.releasenotes', args=('42.0a2', 'aurora'))

    def test_desktop_releasenotes_url(self, mock_reverse):
        """
        Should return the results of reverse with the correct args
        """
        release = models.Release(dict(version='42.0', product='Firefox'))
        assert release.get_absolute_url() == mock_reverse.return_value
        mock_reverse.assert_called_with('firefox.desktop.releasenotes', args=('42.0', 'release'))


@override_settings(RELEASE_NOTES_PATH=RELEASES_PATH, DEV=False)
class TestReleaseModel(TestCase):
    def setUp(self):
        release_cache.clear()

    def test_release_major_version(self):
        rel = models.get_release('firefox', '57.0a1')
        assert rel.major_version == '57'

    def test_get_bug_search_url(self):
        rel = models.get_release('firefox', '57.0a1')
        assert '=Firefox%2057&' in rel.get_bug_search_url()
        rel.product = 'Thunderbird'
        assert '=Thunderbird%2057.0&' in rel.get_bug_search_url()
        rel.bug_search_url = 'custom url'
        assert 'custom url' == rel.get_bug_search_url()

    def test_equivalent_release_for_product(self):
        """Based on the test files the equivalent release for 56 should be 56.0.2"""
        rel = models.get_release('firefox', '56.0', 'release')
        android = rel.equivalent_release_for_product('Firefox for Android')
        assert android.version == '56.0.2'
        assert android.product == 'Firefox for Android'

    def test_equivalent_release_for_product_none_match(self):
        rel = models.get_release('firefox', '45.0esr', 'esr')
        android = rel.equivalent_release_for_product('Firefox for Android')
        assert android is None

    def test_note_fixed_in_release(self):
        rel = models.get_release('firefox', '55.0a1')
        note = rel.notes[11]
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
    def test_is_public_field_processor(self):
        """Should return the real value when DEV is false."""
        rel = models.get_release('firefox for android', '56.0.3')
        assert not rel.is_public
        rel = models.get_release('firefox', '57.0a1')
        assert len(rel.notes) == 4

    @override_settings(DEV=True)
    def test_is_public_field_processor_dev_true(self):
        """Should always be true when DEV is true."""
        rel = models.get_release('firefox for android', '56.0.3')
        assert rel.is_public
        rel = models.get_release('firefox', '57.0a1')
        assert len(rel.notes) == 6


@patch.object(models, 'get_release_file_name')
@patch.object(models, 'get_release_from_file')
class TestGetRelease(TestCase):
    def test_get_release(self, grff_mock, grfn_mock):
        grfn_mock.return_value = 'dude'
        grff_mock.return_value = 'dude is released'
        ret = models.get_release('Firefox', '57.0')
        grfn_mock.assert_called_with('Firefox', models.Release.CHANNELS[0], '57.0')
        grff_mock.assert_called_with('dude')
        assert ret == 'dude is released'

    def test_get_release_esr(self, grff_mock, grfn_mock):
        grfn_mock.return_value = 'dude'
        grff_mock.return_value = 'dude is released'
        ret = models.get_release('Firefox Extended Support Release', '51.0')
        grfn_mock.assert_called_with('firefox', 'esr', '51.0')
        grff_mock.assert_called_with('dude')
        assert ret == 'dude is released'

    def test_get_release_none_match(self, grff_mock, grfn_mock):
        """Make sure the proper exception is raised if no file matches the query"""
        grfn_mock.return_value = None
        with self.assertRaises(models.ReleaseNotFound):
            models.get_release('Firefox', '57.0')

        expected_calls = [call('Firefox', ch, '57.0') for ch in models.Release.CHANNELS]
        grfn_mock.assert_has_calls(expected_calls)

    def test_get_release_none_load(self, grff_mock, grfn_mock):
        """Make sure the proper exception is raised if no file successfully loads"""
        grfn_mock.return_value = 'dude'
        grff_mock.return_value = None
        with self.assertRaises(models.ReleaseNotFound):
            models.get_release('Firefox', '57.0')

        expected_calls = [call('Firefox', ch, '57.0') for ch in models.Release.CHANNELS]
        grfn_mock.assert_has_calls(expected_calls)


@patch.object(models, 'cache')
@patch.object(models, 'get_release_from_file_system')
class TestGetReleaseFromFile(TestCase):
    def test_get_release_from_file(self, grffs_mock, cache_mock):
        cache_mock.get.return_value = 'dude'
        assert models.get_release_from_file('walter') == 'dude'
        cache_mock.get.assert_called_with('walter')
        grffs_mock.assert_not_called()

    def test_get_release_from_file_no_cache(self, grffs_mock, cache_mock):
        cache_mock.get.return_value = None
        grffs_mock.return_value = 'donnie'
        assert models.get_release_from_file('walter') == 'donnie'
        cache_mock.get.assert_called_with('walter')
        grffs_mock.assert_called_with('walter')
        cache_mock.set.assert_called_with('walter', 'donnie', 300)


@override_settings(RELEASE_NOTES_PATH=RELEASES_PATH)
class TestGetReleaseFromFileSystem(TestCase):
    def test_get_release_from_file_system(self):
        filename = models.get_release_file_name('firefox', 'nightly', '57.0a1')
        rel = models.get_release_from_file_system(filename)
        assert rel.product == 'Firefox'
        assert rel.channel == 'Nightly'
        assert rel.version == '57.0a1'

    @patch.object(models, 'codecs')
    def test_get_release_from_file_system_exception(self, codecs_mock):
        codecs_mock.open.side_effect = IOError()
        assert models.get_release_from_file_system('does-not-exist') is None


@patch('os.path.exists')
@patch.object(models, 'get_file_id')
class TestGetReleaseFileName(TestCase):
    def test_get_release_file_name(self, gfi_mock, exists_mock):
        gfi_mock.return_value = 'dude'
        exists_mock.return_value = True
        file_name = os.path.join(settings.RELEASE_NOTES_PATH, 'releases', 'dude.json')
        assert models.get_release_file_name('firefox', 'nightly', '57.0a1') == file_name
        gfi_mock.assert_called_with('firefox', 'nightly', '57.0a1')
        exists_mock.assert_called_with(file_name)

    def test_get_release_file_name_no_exists(self, gfi_mock, exists_mock):
        gfi_mock.return_value = 'dude'
        exists_mock.return_value = False
        file_name = os.path.join(settings.RELEASE_NOTES_PATH, 'releases', 'dude.json')
        assert models.get_release_file_name('firefox', 'nightly', '57.0a1') is None
        gfi_mock.assert_called_with('firefox', 'nightly', '57.0a1')
        exists_mock.assert_called_with(file_name)


class TestGetFileID(TestCase):
    def test_get_file_id(self):
        assert models.get_file_id('Firefox', 'Nightly', '57.0a1') == 'firefox-57.0a1-nightly'
        assert models.get_file_id('Firefox', 'Release', '57.0') == 'firefox-57.0-release'
        assert models.get_file_id('Firefox Extended Support Release', 'ESR', '52.0') == 'firefox-52.0-esr'
        assert models.get_file_id('Firefox for Android', 'Beta', '57.0b2') == 'firefox-for-android-57.0b2-beta'
