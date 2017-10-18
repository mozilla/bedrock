# -*- coding: utf-8 -*-

# Tests for our custom local memory cache backend that does not use pickle
# and instead uses a simple dict for in-memory storage. These were adapted
# from the cache backend tests in Django itself.

from __future__ import unicode_literals

import os
import time
import warnings

from django.core.cache import cache, caches, CacheKeyWarning
from django.test import override_settings, RequestFactory, TestCase


# functions/classes for complex data type tests
def f():
    return 42


class C:
    def m(n):
        return 24


def custom_key_func(key, key_prefix, version):
    "A customized cache key function"
    return 'CUSTOM-' + '-'.join([key_prefix, str(version), key])


_caches_setting_base = {
    'default': {},
    'prefix': {'KEY_PREFIX': 'cacheprefix{}'.format(os.getpid())},
    'v2': {'VERSION': 2},
    'custom_key': {'KEY_FUNCTION': custom_key_func},
    'custom_key2': {'KEY_FUNCTION': 'bedrock.base.tests.test_simple_dict_cache.custom_key_func'},
    'cull': {'OPTIONS': {'MAX_ENTRIES': 30}},
    'zero_cull': {'OPTIONS': {'CULL_FREQUENCY': 0, 'MAX_ENTRIES': 30}},
}


def caches_setting_for_tests(base=None, **params):
    # `base` is used to pull in the memcached config from the original settings,
    # `params` are test specific overrides and `_caches_settings_base` is the
    # base config for the tests.
    # This results in the following search order:
    # params -> _caches_setting_base -> base
    base = base or {}
    setting = dict((k, base.copy()) for k in _caches_setting_base.keys())
    for key, cache_params in setting.items():
        cache_params.update(_caches_setting_base[key])
        cache_params.update(params)
    return setting


@override_settings(CACHES=caches_setting_for_tests(
    BACKEND='bedrock.base.cache.SimpleDictCache',
))
class SimpleDictCacheTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def tearDown(self):
        cache.clear()

    def test_simple(self):
        # Simple cache set/get works
        cache.set("key", "value")
        self.assertEqual(cache.get("key"), "value")

    def test_add(self):
        # A key can be added to a cache
        cache.add("addkey1", "value")
        result = cache.add("addkey1", "newvalue")
        self.assertEqual(result, False)
        self.assertEqual(cache.get("addkey1"), "value")

    def test_prefix(self):
        # Test for same cache key conflicts between shared backend
        cache.set('somekey', 'value')

        # should not be set in the prefixed cache
        self.assertFalse(caches['prefix'].has_key('somekey'))  # noqa

        caches['prefix'].set('somekey', 'value2')

        self.assertEqual(cache.get('somekey'), 'value')
        self.assertEqual(caches['prefix'].get('somekey'), 'value2')

    def test_non_existent(self):
        # Non-existent cache keys return as None/default
        # get with non-existent keys
        self.assertEqual(cache.get("does_not_exist"), None)
        self.assertEqual(cache.get("does_not_exist", "bang!"), "bang!")

    def test_non_none_default(self):
        # Should cache None values if default is not None
        cache.set('is_none', None)
        self.assertIsNone(cache.get('is_none', 'bang!'))

    def test_get_many(self):
        # Multiple cache keys can be returned using get_many
        cache.set('a', 'a')
        cache.set('b', 'b')
        cache.set('c', 'c')
        cache.set('d', 'd')
        self.assertEqual(cache.get_many(['a', 'c', 'd']), {'a': 'a', 'c': 'c', 'd': 'd'})
        self.assertEqual(cache.get_many(['a', 'b', 'e']), {'a': 'a', 'b': 'b'})

    def test_delete(self):
        # Cache keys can be deleted
        cache.set("key1", "spam")
        cache.set("key2", "eggs")
        self.assertEqual(cache.get("key1"), "spam")
        cache.delete("key1")
        self.assertEqual(cache.get("key1"), None)
        self.assertEqual(cache.get("key2"), "eggs")

    def test_has_key(self):
        # The cache can be inspected for cache keys
        cache.set("hello1", "goodbye1")
        self.assertEqual(cache.has_key("hello1"), True)  # noqa
        self.assertEqual(cache.has_key("goodbye1"), False)  # noqa
        cache.set("no_expiry", "here", None)
        self.assertEqual(cache.has_key("no_expiry"), True)  # noqa

    def test_in(self):
        # The in operator can be used to inspect cache contents
        cache.set("hello2", "goodbye2")
        self.assertEqual("hello2" in cache, True)
        self.assertEqual("goodbye2" in cache, False)

    def test_incr(self):
        # Cache values can be incremented
        cache.set('answer', 41)
        self.assertEqual(cache.incr('answer'), 42)
        self.assertEqual(cache.get('answer'), 42)
        self.assertEqual(cache.incr('answer', 10), 52)
        self.assertEqual(cache.get('answer'), 52)
        self.assertEqual(cache.incr('answer', -10), 42)
        self.assertRaises(ValueError, cache.incr, 'does_not_exist')

    def test_decr(self):
        # Cache values can be decremented
        cache.set('answer', 43)
        self.assertEqual(cache.decr('answer'), 42)
        self.assertEqual(cache.get('answer'), 42)
        self.assertEqual(cache.decr('answer', 10), 32)
        self.assertEqual(cache.get('answer'), 32)
        self.assertEqual(cache.decr('answer', -10), 42)
        self.assertRaises(ValueError, cache.decr, 'does_not_exist')

    def test_close(self):
        self.assertTrue(hasattr(cache, 'close'))
        cache.close()

    def test_data_types(self):
        # Many different data types can be cached
        stuff = {
            'string': 'this is a string',
            'int': 42,
            'list': [1, 2, 3, 4],
            'tuple': (1, 2, 3, 4),
            'dict': {'A': 1, 'B': 2},
            'function': f,
            'class': C,
        }
        cache.set("stuff", stuff)
        self.assertEqual(cache.get("stuff"), stuff)

    def test_expiration(self):
        # Cache values can be set to expire
        cache.set('expire1', 'very quickly', 1)
        cache.set('expire2', 'very quickly', 1)
        cache.set('expire3', 'very quickly', 1)

        time.sleep(2)
        self.assertEqual(cache.get("expire1"), None)

        cache.add("expire2", "newvalue")
        self.assertEqual(cache.get("expire2"), "newvalue")
        self.assertEqual(cache.has_key("expire3"), False)  # noqa

    def test_unicode(self):
        # Unicode values can be cached
        stuff = {
            'ascii': 'ascii_value',
            'unicode_ascii': 'Iñtërnâtiônàlizætiøn1',
            'Iñtërnâtiônàlizætiøn': 'Iñtërnâtiônàlizætiøn2',
            'ascii2': {'x': 1}
        }
        # Test `set`
        for (key, value) in stuff.items():
            cache.set(key, value)
            self.assertEqual(cache.get(key), value)

        # Test `add`
        for (key, value) in stuff.items():
            cache.delete(key)
            cache.add(key, value)
            self.assertEqual(cache.get(key), value)

        # Test `set_many`
        for (key, value) in stuff.items():
            cache.delete(key)
        cache.set_many(stuff)
        for (key, value) in stuff.items():
            self.assertEqual(cache.get(key), value)

    def test_binary_string(self):
        # Binary strings should be cacheable
        from zlib import compress, decompress

        value = 'value_to_be_compressed'
        compressed_value = compress(value.encode())

        # Test set
        cache.set('binary1', compressed_value)
        compressed_result = cache.get('binary1')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

        # Test add
        cache.add('binary1-add', compressed_value)
        compressed_result = cache.get('binary1-add')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

        # Test set_many
        cache.set_many({'binary1-set_many': compressed_value})
        compressed_result = cache.get('binary1-set_many')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

    def test_set_many(self):
        # Multiple keys can be set using set_many
        cache.set_many({"key1": "spam", "key2": "eggs"})
        self.assertEqual(cache.get("key1"), "spam")
        self.assertEqual(cache.get("key2"), "eggs")

    def test_set_many_expiration(self):
        # set_many takes a second ``timeout`` parameter
        cache.set_many({"key1": "spam", "key2": "eggs"}, 1)
        time.sleep(2)
        self.assertEqual(cache.get("key1"), None)
        self.assertEqual(cache.get("key2"), None)

    def test_delete_many(self):
        # Multiple keys can be deleted using delete_many
        cache.set("key1", "spam")
        cache.set("key2", "eggs")
        cache.set("key3", "ham")
        cache.delete_many(["key1", "key2"])
        self.assertEqual(cache.get("key1"), None)
        self.assertEqual(cache.get("key2"), None)
        self.assertEqual(cache.get("key3"), "ham")

    def test_clear(self):
        # The cache can be emptied using clear
        cache.set("key1", "spam")
        cache.set("key2", "eggs")
        cache.clear()
        self.assertEqual(cache.get("key1"), None)
        self.assertEqual(cache.get("key2"), None)

    def test_long_timeout(self):
        '''
        Using a timeout greater than 30 days makes memcached think
        it is an absolute expiration timestamp instead of a relative
        offset. Test that we honour this convention. Refs #12399.
        '''
        cache.set('key1', 'eggs', 60 * 60 * 24 * 30 + 1)  # 30 days + 1 second
        self.assertEqual(cache.get('key1'), 'eggs')

        cache.add('key2', 'ham', 60 * 60 * 24 * 30 + 1)
        self.assertEqual(cache.get('key2'), 'ham')

        cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, 60 * 60 * 24 * 30 + 1)
        self.assertEqual(cache.get('key3'), 'sausage')
        self.assertEqual(cache.get('key4'), 'lobster bisque')

    def test_forever_timeout(self):
        '''
        Passing in None into timeout results in a value that is cached forever
        '''
        cache.set('key1', 'eggs', None)
        self.assertEqual(cache.get('key1'), 'eggs')

        cache.add('key2', 'ham', None)
        self.assertEqual(cache.get('key2'), 'ham')
        added = cache.add('key1', 'new eggs', None)
        self.assertEqual(added, False)
        self.assertEqual(cache.get('key1'), 'eggs')

        cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, None)
        self.assertEqual(cache.get('key3'), 'sausage')
        self.assertEqual(cache.get('key4'), 'lobster bisque')

    def test_zero_timeout(self):
        '''
        Passing in zero into timeout results in a value that is not cached
        '''
        cache.set('key1', 'eggs', 0)
        self.assertEqual(cache.get('key1'), None)

        cache.add('key2', 'ham', 0)
        self.assertEqual(cache.get('key2'), None)

        cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, 0)
        self.assertEqual(cache.get('key3'), None)
        self.assertEqual(cache.get('key4'), None)

    def test_float_timeout(self):
        # Make sure a timeout given as a float doesn't crash anything.
        cache.set("key1", "spam", 100.2)
        self.assertEqual(cache.get("key1"), "spam")

    def _perform_cull_test(self, cull_cache, initial_count, final_count):
        # Create initial cache key entries. This will overflow the cache,
        # causing a cull.
        for i in range(1, initial_count):
            cull_cache.set('cull%d' % i, 'value', 1000)
        count = 0
        # Count how many keys are left in the cache.
        for i in range(1, initial_count):
            if cull_cache.has_key('cull%d' % i):  # noqa
                count = count + 1
        self.assertEqual(count, final_count)

    def test_cull(self):
        self._perform_cull_test(caches['cull'], 50, 29)

    def test_zero_cull(self):
        self._perform_cull_test(caches['zero_cull'], 50, 19)

    def test_invalid_keys(self):
        """
        All the builtin backends (except memcached, see below) should warn on
        keys that would be refused by memcached. This encourages portable
        caching code without making it too difficult to use production backends
        with more liberal key rules. Refs #6447.
        """
        # mimic custom ``make_key`` method being defined since the default will
        # never show the below warnings
        def func(key, *args):
            return key

        old_func = cache.key_func
        cache.key_func = func

        try:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                # memcached does not allow whitespace or control characters in keys
                cache.set('key with spaces', 'value')
                self.assertEqual(len(w), 2)
                self.assertIsInstance(w[0].message, CacheKeyWarning)
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                # memcached limits key length to 250
                cache.set('a' * 251, 'value')
                self.assertEqual(len(w), 1)
                self.assertIsInstance(w[0].message, CacheKeyWarning)
        finally:
            cache.key_func = old_func

    def test_cache_versioning_get_set(self):
        # set, using default version = 1
        cache.set('answer1', 42)
        self.assertEqual(cache.get('answer1'), 42)
        self.assertEqual(cache.get('answer1', version=1), 42)
        self.assertEqual(cache.get('answer1', version=2), None)

        self.assertEqual(caches['v2'].get('answer1'), None)
        self.assertEqual(caches['v2'].get('answer1', version=1), 42)
        self.assertEqual(caches['v2'].get('answer1', version=2), None)

        # set, default version = 1, but manually override version = 2
        cache.set('answer2', 42, version=2)
        self.assertEqual(cache.get('answer2'), None)
        self.assertEqual(cache.get('answer2', version=1), None)
        self.assertEqual(cache.get('answer2', version=2), 42)

        self.assertEqual(caches['v2'].get('answer2'), 42)
        self.assertEqual(caches['v2'].get('answer2', version=1), None)
        self.assertEqual(caches['v2'].get('answer2', version=2), 42)

        # v2 set, using default version = 2
        caches['v2'].set('answer3', 42)
        self.assertEqual(cache.get('answer3'), None)
        self.assertEqual(cache.get('answer3', version=1), None)
        self.assertEqual(cache.get('answer3', version=2), 42)

        self.assertEqual(caches['v2'].get('answer3'), 42)
        self.assertEqual(caches['v2'].get('answer3', version=1), None)
        self.assertEqual(caches['v2'].get('answer3', version=2), 42)

        # v2 set, default version = 2, but manually override version = 1
        caches['v2'].set('answer4', 42, version=1)
        self.assertEqual(cache.get('answer4'), 42)
        self.assertEqual(cache.get('answer4', version=1), 42)
        self.assertEqual(cache.get('answer4', version=2), None)

        self.assertEqual(caches['v2'].get('answer4'), None)
        self.assertEqual(caches['v2'].get('answer4', version=1), 42)
        self.assertEqual(caches['v2'].get('answer4', version=2), None)

    def test_cache_versioning_add(self):

        # add, default version = 1, but manually override version = 2
        cache.add('answer1', 42, version=2)
        self.assertEqual(cache.get('answer1', version=1), None)
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.add('answer1', 37, version=2)
        self.assertEqual(cache.get('answer1', version=1), None)
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.add('answer1', 37, version=1)
        self.assertEqual(cache.get('answer1', version=1), 37)
        self.assertEqual(cache.get('answer1', version=2), 42)

        # v2 add, using default version = 2
        caches['v2'].add('answer2', 42)
        self.assertEqual(cache.get('answer2', version=1), None)
        self.assertEqual(cache.get('answer2', version=2), 42)

        caches['v2'].add('answer2', 37)
        self.assertEqual(cache.get('answer2', version=1), None)
        self.assertEqual(cache.get('answer2', version=2), 42)

        caches['v2'].add('answer2', 37, version=1)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), 42)

        # v2 add, default version = 2, but manually override version = 1
        caches['v2'].add('answer3', 42, version=1)
        self.assertEqual(cache.get('answer3', version=1), 42)
        self.assertEqual(cache.get('answer3', version=2), None)

        caches['v2'].add('answer3', 37, version=1)
        self.assertEqual(cache.get('answer3', version=1), 42)
        self.assertEqual(cache.get('answer3', version=2), None)

        caches['v2'].add('answer3', 37)
        self.assertEqual(cache.get('answer3', version=1), 42)
        self.assertEqual(cache.get('answer3', version=2), 37)

    def test_cache_versioning_has_key(self):
        cache.set('answer1', 42)

        # has_key
        self.assertTrue(cache.has_key('answer1'))  # noqa
        self.assertTrue(cache.has_key('answer1', version=1))  # noqa
        self.assertFalse(cache.has_key('answer1', version=2))  # noqa

        self.assertFalse(caches['v2'].has_key('answer1'))  # noqa
        self.assertTrue(caches['v2'].has_key('answer1', version=1))  # noqa
        self.assertFalse(caches['v2'].has_key('answer1', version=2))  # noqa

    def test_cache_versioning_delete(self):
        cache.set('answer1', 37, version=1)
        cache.set('answer1', 42, version=2)
        cache.delete('answer1')
        self.assertEqual(cache.get('answer1', version=1), None)
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.set('answer2', 37, version=1)
        cache.set('answer2', 42, version=2)
        cache.delete('answer2', version=2)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), None)

        cache.set('answer3', 37, version=1)
        cache.set('answer3', 42, version=2)
        caches['v2'].delete('answer3')
        self.assertEqual(cache.get('answer3', version=1), 37)
        self.assertEqual(cache.get('answer3', version=2), None)

        cache.set('answer4', 37, version=1)
        cache.set('answer4', 42, version=2)
        caches['v2'].delete('answer4', version=1)
        self.assertEqual(cache.get('answer4', version=1), None)
        self.assertEqual(cache.get('answer4', version=2), 42)

    def test_cache_versioning_incr_decr(self):
        cache.set('answer1', 37, version=1)
        cache.set('answer1', 42, version=2)
        cache.incr('answer1')
        self.assertEqual(cache.get('answer1', version=1), 38)
        self.assertEqual(cache.get('answer1', version=2), 42)
        cache.decr('answer1')
        self.assertEqual(cache.get('answer1', version=1), 37)
        self.assertEqual(cache.get('answer1', version=2), 42)

        cache.set('answer2', 37, version=1)
        cache.set('answer2', 42, version=2)
        cache.incr('answer2', version=2)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), 43)
        cache.decr('answer2', version=2)
        self.assertEqual(cache.get('answer2', version=1), 37)
        self.assertEqual(cache.get('answer2', version=2), 42)

        cache.set('answer3', 37, version=1)
        cache.set('answer3', 42, version=2)
        caches['v2'].incr('answer3')
        self.assertEqual(cache.get('answer3', version=1), 37)
        self.assertEqual(cache.get('answer3', version=2), 43)
        caches['v2'].decr('answer3')
        self.assertEqual(cache.get('answer3', version=1), 37)
        self.assertEqual(cache.get('answer3', version=2), 42)

        cache.set('answer4', 37, version=1)
        cache.set('answer4', 42, version=2)
        caches['v2'].incr('answer4', version=1)
        self.assertEqual(cache.get('answer4', version=1), 38)
        self.assertEqual(cache.get('answer4', version=2), 42)
        caches['v2'].decr('answer4', version=1)
        self.assertEqual(cache.get('answer4', version=1), 37)
        self.assertEqual(cache.get('answer4', version=2), 42)

    def test_cache_versioning_get_set_many(self):
        # set, using default version = 1
        cache.set_many({'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache.get_many(['ford1', 'arthur1']),
                         {'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache.get_many(['ford1', 'arthur1'], version=1),
                         {'ford1': 37, 'arthur1': 42})
        self.assertEqual(cache.get_many(['ford1', 'arthur1'], version=2), {})

        self.assertEqual(caches['v2'].get_many(['ford1', 'arthur1']), {})
        self.assertEqual(caches['v2'].get_many(['ford1', 'arthur1'], version=1),
                         {'ford1': 37, 'arthur1': 42})
        self.assertEqual(caches['v2'].get_many(['ford1', 'arthur1'], version=2), {})

        # set, default version = 1, but manually override version = 2
        cache.set_many({'ford2': 37, 'arthur2': 42}, version=2)
        self.assertEqual(cache.get_many(['ford2', 'arthur2']), {})
        self.assertEqual(cache.get_many(['ford2', 'arthur2'], version=1), {})
        self.assertEqual(cache.get_many(['ford2', 'arthur2'], version=2),
                         {'ford2': 37, 'arthur2': 42})

        self.assertEqual(caches['v2'].get_many(['ford2', 'arthur2']),
                         {'ford2': 37, 'arthur2': 42})
        self.assertEqual(caches['v2'].get_many(['ford2', 'arthur2'], version=1), {})
        self.assertEqual(caches['v2'].get_many(['ford2', 'arthur2'], version=2),
                         {'ford2': 37, 'arthur2': 42})

        # v2 set, using default version = 2
        caches['v2'].set_many({'ford3': 37, 'arthur3': 42})
        self.assertEqual(cache.get_many(['ford3', 'arthur3']), {})
        self.assertEqual(cache.get_many(['ford3', 'arthur3'], version=1), {})
        self.assertEqual(cache.get_many(['ford3', 'arthur3'], version=2),
                         {'ford3': 37, 'arthur3': 42})

        self.assertEqual(caches['v2'].get_many(['ford3', 'arthur3']),
                         {'ford3': 37, 'arthur3': 42})
        self.assertEqual(caches['v2'].get_many(['ford3', 'arthur3'], version=1), {})
        self.assertEqual(caches['v2'].get_many(['ford3', 'arthur3'], version=2),
                         {'ford3': 37, 'arthur3': 42})

        # v2 set, default version = 2, but manually override version = 1
        caches['v2'].set_many({'ford4': 37, 'arthur4': 42}, version=1)
        self.assertEqual(cache.get_many(['ford4', 'arthur4']),
                         {'ford4': 37, 'arthur4': 42})
        self.assertEqual(cache.get_many(['ford4', 'arthur4'], version=1),
                         {'ford4': 37, 'arthur4': 42})
        self.assertEqual(cache.get_many(['ford4', 'arthur4'], version=2), {})

        self.assertEqual(caches['v2'].get_many(['ford4', 'arthur4']), {})
        self.assertEqual(caches['v2'].get_many(['ford4', 'arthur4'], version=1),
                         {'ford4': 37, 'arthur4': 42})
        self.assertEqual(caches['v2'].get_many(['ford4', 'arthur4'], version=2), {})

    def test_incr_version(self):
        cache.set('answer', 42, version=2)
        self.assertEqual(cache.get('answer'), None)
        self.assertEqual(cache.get('answer', version=1), None)
        self.assertEqual(cache.get('answer', version=2), 42)
        self.assertEqual(cache.get('answer', version=3), None)

        self.assertEqual(cache.incr_version('answer', version=2), 3)
        self.assertEqual(cache.get('answer'), None)
        self.assertEqual(cache.get('answer', version=1), None)
        self.assertEqual(cache.get('answer', version=2), None)
        self.assertEqual(cache.get('answer', version=3), 42)

        caches['v2'].set('answer2', 42)
        self.assertEqual(caches['v2'].get('answer2'), 42)
        self.assertEqual(caches['v2'].get('answer2', version=1), None)
        self.assertEqual(caches['v2'].get('answer2', version=2), 42)
        self.assertEqual(caches['v2'].get('answer2', version=3), None)

        self.assertEqual(caches['v2'].incr_version('answer2'), 3)
        self.assertEqual(caches['v2'].get('answer2'), None)
        self.assertEqual(caches['v2'].get('answer2', version=1), None)
        self.assertEqual(caches['v2'].get('answer2', version=2), None)
        self.assertEqual(caches['v2'].get('answer2', version=3), 42)

        self.assertRaises(ValueError, cache.incr_version, 'does_not_exist')

    def test_decr_version(self):
        cache.set('answer', 42, version=2)
        self.assertEqual(cache.get('answer'), None)
        self.assertEqual(cache.get('answer', version=1), None)
        self.assertEqual(cache.get('answer', version=2), 42)

        self.assertEqual(cache.decr_version('answer', version=2), 1)
        self.assertEqual(cache.get('answer'), 42)
        self.assertEqual(cache.get('answer', version=1), 42)
        self.assertEqual(cache.get('answer', version=2), None)

        caches['v2'].set('answer2', 42)
        self.assertEqual(caches['v2'].get('answer2'), 42)
        self.assertEqual(caches['v2'].get('answer2', version=1), None)
        self.assertEqual(caches['v2'].get('answer2', version=2), 42)

        self.assertEqual(caches['v2'].decr_version('answer2'), 1)
        self.assertEqual(caches['v2'].get('answer2'), None)
        self.assertEqual(caches['v2'].get('answer2', version=1), 42)
        self.assertEqual(caches['v2'].get('answer2', version=2), None)

        self.assertRaises(ValueError, cache.decr_version, 'does_not_exist', version=2)

    def test_custom_key_func(self):
        # Two caches with different key functions aren't visible to each other
        cache.set('answer1', 42)
        self.assertEqual(cache.get('answer1'), 42)
        self.assertEqual(caches['custom_key'].get('answer1'), None)
        self.assertEqual(caches['custom_key2'].get('answer1'), None)

        caches['custom_key'].set('answer2', 42)
        self.assertEqual(cache.get('answer2'), None)
        self.assertEqual(caches['custom_key'].get('answer2'), 42)
        self.assertEqual(caches['custom_key2'].get('answer2'), 42)

    @override_settings(CACHES={
        'default': {'BACKEND': 'bedrock.base.cache.SimpleDictCache'},
        'other': {
            'BACKEND': 'bedrock.base.cache.SimpleDictCache',
            'LOCATION': 'other'
        },
    })
    def test_multiple_caches(self):
        """Check that multiple locmem caches are isolated"""
        cache.set('value', 42)
        self.assertEqual(caches['default'].get('value'), 42)
        self.assertEqual(caches['other'].get('value'), None)

    def test_incr_decr_timeout(self):
        """incr/decr does not modify expiry time (matches memcached behavior)"""
        key = 'value'
        _key = cache.make_key(key)
        cache.set(key, 1, timeout=cache.default_timeout * 10)
        expire = cache._expire_info[_key]
        cache.incr(key)
        self.assertEqual(expire, cache._expire_info[_key])
        cache.decr(key)
        self.assertEqual(expire, cache._expire_info[_key])
