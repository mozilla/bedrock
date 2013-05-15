# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

from funfactory.middleware import LocaleURLMiddleware


class TabzillaLocaleURLMiddleware(LocaleURLMiddleware):
    def process_request(self, request):
        resp = super(TabzillaLocaleURLMiddleware, self).process_request(request)

        # no locale redirect happening
        if resp is None:
            return resp

        is_enabled = not settings.TEMPLATE_DEBUG and settings.CDN_BASE_URL
        is_interesting = 'tabzilla.js' in resp.get('location', '')
        if is_enabled and is_interesting:
            # CDN URL should be protocol relative, but that won't work
            # in a Location header.
            protocol = 'https:' if request.is_secure() else 'http:'
            cdn_base = protocol + settings.CDN_BASE_URL
            resp['location'] = cdn_base + resp['location']

        return resp
