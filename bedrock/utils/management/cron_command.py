# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""
A Django management command class that handles locking so it doesn't
trigger multiple times when used inside of an external script, such as a
cron job.

If a lock already exists, the command will exit silently.
"""
import abc
from contextlib import contextmanager

from django.core.cache import cache
from django.core.management.base import BaseCommand


@contextmanager
def cache_lock(lock_key):
    """
    A context manager that attempts to create a lock in cache.

    Returns True if a lock was established, or False if a lock already
    existed.
    """
    lock = cache.get(lock_key)
    if not lock:
        cache.set(lock_key, True, 60)
        try:
            yield True
        finally:
            cache.delete(lock_key)
    else:
        yield False


class CronCommand(BaseCommand):
    lock_key = 'cron-command'

    def get_lock_key(self):
        return 'command-lock:' + self.lock_key

    def get_lock(self):
        return cache_lock(self.get_lock_key())

    def handle(self, *args, **options):
        with self.get_lock() as safe:
            if safe:
                self.handle_safe(**options)

    @abc.abstractmethod
    def handle_safe(self, *args, **options):
        """
        The handle method, but with the assurance that it isn't being executed
        by another process.
        """
