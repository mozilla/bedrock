import time

from mock import Mock, patch

from django.core.cache import caches

from bedrock.mozorg.tests import TestCase
from bedrock.releasenotes import utils


release_cache = caches['release-notes']


@patch.object(utils, 'GitRepo')
class TestGetDataVersion(TestCase):
    def test_get_data_version(self, git_mock):
        git_mock().get_db_latest.return_value = 'El Dudarino'
        assert utils.get_data_version() == 'El Dudarino'

    def test_get_data_version_not_found(self, git_mock):
        git_mock().get_db_latest.return_value = None
        assert utils.get_data_version() == 'default'


@patch.object(utils, 'get_data_version')
class TestReleaseMemoizer(TestCase):
    def setUp(self):
        release_cache.clear()

    def test_calls_version_after_cache_timeout(self, gdv_cache):
        def mem_func():
            pass

        gdv_cache.return_value = 'dude'
        memoizer = utils.ReleaseMemoizer(version_timeout=0.1)
        memoizer._memoize_version(mem_func)
        memoizer._memoize_version(mem_func)
        time.sleep(0.2)
        memoizer._memoize_version(mem_func)
        assert gdv_cache.call_count == 2

    def test_calls_function_when_version_changes(self, gdv_cache):
        """Memoized function should be called after timeout or version change.

        Also demonstrates that even None return values are cached."""
        counter = Mock()
        memoizer = utils.ReleaseMemoizer(version_timeout=0.1)
        gdv_cache.side_effect = ['thing1', 'thing1', 'thing2', 'thing2']

        @memoizer.memoize(1)
        def mem_func():
            counter()
            return None

        mem_func()
        # cached
        mem_func()
        time.sleep(0.2)
        # cached, but checked the version
        mem_func()
        time.sleep(0.2)
        # not cached because the version changed
        mem_func()
        time.sleep(1.1)
        # not cached because timeout
        mem_func()

        # function should have been called 3 times
        assert counter.call_count == 3
        # version should have been called 4 times
        assert gdv_cache.call_count == 4
