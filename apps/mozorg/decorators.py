# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from functools import wraps
from hashlib import md5

from django.utils.http import http_date


def cache_control_expires(num_hours):
    """
    Set the appropriate Cache-Control, Expires, and ETag headers for the given
    number of hours.
    """
    num_seconds = num_hours * 60 * 60

    def decorator(func):

        @wraps(func)
        def inner(request, *args, **kwargs):
            response = func(request, *args, **kwargs)
            response['Cache-Control'] = 'max-age=%d' % num_seconds
            response['Expires'] = http_date(time.time() + num_seconds)
            response['ETag'] = '"%s"' % md5(response.content).hexdigest()
            return response
        return inner
    return decorator
