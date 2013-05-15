# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from commonware.decorators import xframe_allow

from django.conf import settings
from django.shortcuts import redirect

from bedrock.facebookapps import utils


@xframe_allow
def tab_redirect(request, redirect_type='server'):
    app_data_query_string = utils.app_data_query_string_encode(request.GET)
    # Cast into unicode string to avoid `join` treating it as a `__proxy__`
    tab_url = unicode(settings.FACEBOOK_TAB_URL)
    final_url = ('?'.join([tab_url, app_data_query_string])
                 if app_data_query_string else tab_url)

    if redirect_type == 'js':
        return utils.js_redirect(final_url, request)

    return redirect(final_url)
