# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib
from functools import wraps

from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from funfactory import urlresolvers

from bedrock.facebookapps import utils


def facebook_locale(view_fn):
    """
    Redirects to Facebook user's locale retrieved from `signed_request` or
    best supported approximation of it.
    """
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _decorated_view(request, *args, **kwargs):
        # Get locale from Facebook's `signed_request`
        signed_request = utils.unwrap_signed_request(request)
        try:
            facebook_locale = signed_request['user']['locale']
        except KeyError:
            pass
        else:
            # If user's locale isn't supported, get the next best one.
            # Defaults to en-US if no locale in same language as the
            # user's is found.
            best_locale = utils.get_best_locale(facebook_locale)

            prefix = urlresolvers.get_url_prefix()

            # Compare locales in lowercase just in case. Heh.
            # If we aren't using the best locale, redirect to it
            if prefix.locale.lower() != best_locale.lower():
                prefix.locale = best_locale
                locale_url = prefix.fix(request.path_info)
                query_string = urllib.urlencode(request.GET)
                final_url = ('?'.join([locale_url, query_string])
                             if query_string else locale_url)
                return redirect(final_url)

        return view_fn(request, *args, **kwargs)

    return _decorated_view


def extract_app_data(view_fn):
    """
    Extracts custom data from Facebook's `signed_request` and places it in
    the `request.GET` dictionary.
    """
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _decorated_view(request, *args, **kwargs):
        # Get custom data from Facebook's `signed_request`
        signed_request = utils.unwrap_signed_request(request)
        try:
            app_data = signed_request['app_data']
        except KeyError:
            pass
        else:
            # Add it to the GET dictionary
            new_get = request.GET.copy()
            new_get.update(app_data)
            request.GET = new_get

        return view_fn(request, *args, **kwargs)

    return _decorated_view
