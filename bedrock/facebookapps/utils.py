# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import urllib
from base64 import urlsafe_b64decode

from django.conf import settings
from django.utils.translation import get_language

import commonware.log
import tower
from lib import l10n_utils


log = commonware.log.getLogger('facebookapps.utils')


def unwrap_signed_request(request):
    """
    Decodes and returns Facebook's `signed_request` data.

    See https://developers.facebook.com/docs/howtos/login/signed-request/
    """
    try:
        encoded_signed_request = request.REQUEST['signed_request']
    except KeyError:
        log.exception('signed_request not set')
        return {}

    encoded_string_data = encoded_signed_request.partition('.')[2]
    # Pad with `=` to make string length a multiple of 4
    # and thus prevent a base64 error
    padding = ''.ljust(4 - len(encoded_string_data) % 4, '=')
    padded_string = ''.join([encoded_string_data, padding])
    # Convert to byte data for base64
    encoded_byte_data = bytes(padded_string)
    signed_request = json.loads(urlsafe_b64decode(encoded_byte_data))

    # Change Facebook locale's underscore to hyphen
    # ex. `en_US` to `en-US`
    try:
        locale = signed_request['user']['locale']
    except KeyError:
        locale = None

    if locale:
        signed_request['user']['locale'] = locale.replace('_', '-')

    return signed_request


def app_data_query_string_encode(app_data):
    return urllib.urlencode([('app_data[{key}]'.format(key=key), value)
        for key, value in app_data.items()])


def get_best_locale(locale):
    """
    Returns the most appropriate locale from the list of supported locales.
    This can either be the locale itself (if it's supported), the main locale
    for that language if any or failing any of that the default `en-US`.

    Adapted from `activate_locale` in Affiliates (http://bit.ly/17if6nh).
    """
    # Compare using lowercase locales since they become lowercase once
    # activated.
    supported_locales = [loc.lower() for loc in settings.FACEBOOK_LOCALES]

    # HACK: It's not totally clear to me where Django or tower do the matching
    # that equates locales like es-LA to es, and I'm scared enough of getting
    # it wrong to want to avoid it for the first release. So instead, we'll
    # activate the requested locale, and then check what locale got chosen by
    # django as the usable locale, and match that against our locale
    # whitelist.
    # TODO: Properly filter out locales prior to calling activate.
    old_locale = get_language()
    tower.activate(locale)
    lang = get_language()

    if lang.lower() not in supported_locales:
        # Try to activate just the language and use the resulting locale
        lang_prefix = lang.split('-')[0]
        tower.activate(lang_prefix)
        lang = get_language()

        if lang.lower() not in supported_locales:
            # Finally, try to find a locale with that language in the supported
            # locales. Otherwise, use default en-US.
            try:
                lang = next(locale for locale in settings.FACEBOOK_LOCALES
                    if locale.startswith(lang_prefix))
            except StopIteration:
                lang = 'en-US'

    tower.activate(old_locale)
    return lang


def js_redirect(redirect_url, request):
    return l10n_utils.render(request, 'facebookapps/js-redirect.html',
        {'redirect_url': redirect_url})
