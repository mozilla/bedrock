from functools import wraps

from django.conf import settings
from django.core.cache import cache

from bedrock.events.models import Event


CACHE_TIMEOUT = getattr(settings, 'EVENTS_CACHE_TIMEOUT', 15 * 60)


def cache_memoized(obj):
    """
    Uses the django default cache backend to memoize results from function,
    method, or class calls. Decorated function will accept a 'force_cache_refresh'
    kwarg which will do exactly that if True. Results must be pickleable.
    Caches results unique to args, but *not* to kwargs.
    """
    @wraps(obj)
    def wrapped(*args, **kwargs):
        # NOTE: this ignores kwargs for caching purposes
        cache_key = ':'.join([__name__, obj.__name__] + [str(a) for a in args])
        force_cache_refresh = kwargs.pop('force_cache_refresh', False)
        if not force_cache_refresh:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        result = obj(*args, **kwargs)
        cache.set(cache_key, result, timeout=CACHE_TIMEOUT)
        return result
    return wrapped


@cache_memoized
def future_event_count():
    return Event.objects.future().count()


@cache_memoized
def future_events():
    return list(Event.objects.future())


@cache_memoized
def next_few_events(count):
    return list(Event.objects.future()[:count])


def next_event():
    # If there is no next event we want to return None, which
    # is not cacheable, but next_few_events will cache an empty list
    # for us in that case.
    events = next_few_events(1)
    return events[0] if events else None
