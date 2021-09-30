# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from functools import wraps

from django.utils.cache import patch_response_headers


def cache_control_expires(num_hours):
    """
    Set the appropriate Cache-Control and Expires headers for the given
    number of hours.
    """
    num_seconds = int(num_hours * 60 * 60)

    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            patch_response_headers(response, num_seconds)
            return response

        return inner

    return decorator
