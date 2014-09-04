# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.core.cache.backends.locmem import LocMemCache

from django_statsd.clients import statsd


class L10nCache(LocMemCache):
    def _cull(self):
        statsd.incr('cache.l10n.cull')
        super(L10nCache, self)._cull()

    def _set(self, key, value, timeout=None):
        statsd.gauge('cache.l10n.entries', len(self._cache), 0.1)
        super(L10nCache, self)._set(key, value, timeout)
