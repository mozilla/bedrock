# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from django.conf import settings
from django.core.cache import caches
from django.core.cache.backends.locmem import DEFAULT_TIMEOUT, LocMemCache

from bedrock.base import metrics

logger = logging.getLogger(__name__)


class SimpleDictCache(LocMemCache):
    """A local memory cache that doesn't pickle values.

    Only for use with simple immutable data structures that can be
    inserted into a dict. If you put something mutable in here, then
    mutate it elsewhere, the cached data will also be changed.
    """

    def __init__(self, name, params):
        super().__init__(name, params)
        self._name = name

    def _set(self, key, value, timeout=DEFAULT_TIMEOUT):
        super()._set(key, value, timeout)
        if len(self._cache) % 10 == 0:
            metrics.gauge("cache.size", value=len(self._cache), tags=[f"cache:{self._name}"])

    def _cull(self):
        super()._cull()
        metrics.incr("cache.cull", tags=[f"cache:{self._name}"])

    def add(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        with self._lock:
            if self._has_expired(key):
                self._set(key, value, timeout)
                return True
            return False

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        value = default
        with self._lock:
            if not self._has_expired(key):
                value = self._cache[key]
        if value is not default:
            return value

        with self._lock:
            try:
                del self._cache[key]
                del self._expire_info[key]
            except KeyError:
                pass
            return default

    def set(self, key, value, timeout=DEFAULT_TIMEOUT, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        with self._lock:
            self._set(key, value, timeout)

    def incr(self, key, delta=1, version=None):
        value = self.get(key, version=version)
        if value is None:
            raise ValueError(f"Key '{key}' not found")
        new_value = value + delta
        key = self.make_key(key, version=version)
        with self._lock:
            self._cache[key] = new_value
        return new_value


# === HYBRID CACHE BEHAVIOUR ===
#
# Our "hybrid cache" approach uses SimpleDictCache as a local, read-through
# cache on the pod, which falls back to get values from a distributed
# DB-backed cache.
# The DB-backed cache is NOT a read-through cache and only has its values
# set explicitly.

local_cache = caches["default"]  # This is the SimpleDictCache
db_cache = caches["db"]


def get_from_hybrid_cache(key, default=None):
    """
    Retrieve a value from the hybrid cache. First checks local cache, then falls
    back to DB cache.

    If found in DB cache, the value is added to local cache for faster subsequent
    access.

    This can be called from any code, because it does not require write access to
    the DB.

    :param key: The cache key to retrieve.
    :param default: Default value to return if the key is not found in either cache.

    :return: The cached value, or the default if the key is not found.
    """
    # Check local cache
    value = local_cache.get(key)
    if value is not None:
        return value

    # Check DB cache and if it has a value, pop it into
    # the local cache en route to returning the value
    value = db_cache.get(key)
    if value is not None:
        local_cache.set(
            key,
            value,
            timeout=settings.CACHE_TIME_SHORT,
        )
        return value

    return default


def set_in_hybrid_cache(key, value, timeout=None):
    """
    Set a value in the hybrid cache.

    Writes to both the local cache and the DB cache.

    IMPORTANT: this should only be called from somewhere with DB-write access -
    i.e. the CMS deployment pod – if it is called from a Web deployment pod, it
    will only set the local-memory cache and also log an exception, because
    there will be unpredictable results if you're tryint to cache cache
    something that should be available across pods -- and if you're not you
    should just use the regular 'default' local-memory cache directly.

    :param key: The cache key to set.
    :param value: The value to cache.
    :param timeout: Timeout for DB cache in seconds (local cache will use a shorter timeout by default).
    """
    # Set in DB cache first, with the provided optional timeout.
    # In settings we have a timeout of None, so it will never expire
    # but still can be replaced (via this helper function)

    try:
        db_cache.set(
            key,
            value,
            timeout=timeout,
        )
    except Exception as ex:
        # Cope with the DB cache not being available - eg
        logger.exception(f"Could not set value in DB-backed cache: {ex}")

    # Set in local cache with a short timeout
    local_cache.set(
        key,
        value,
        timeout=settings.CACHE_TIME_SHORT,
    )
