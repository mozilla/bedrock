from django.core.cache.backends.locmem import LocMemCache, DEFAULT_TIMEOUT


class SimpleDictCache(LocMemCache):
    """A local memory cache that doesn't pickle values.

    Only for use with simple immutable data structures that can be
    inserted into a dict.
    """
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
            raise ValueError("Key '%s' not found" % key)
        new_value = value + delta
        key = self.make_key(key, version=version)
        with self._lock:
            self._cache[key] = new_value
        return new_value
