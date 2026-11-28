# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import Resolver404

from bedrock.base.i18n import split_path_and_normalize_language

from .util import get_resolver


class RedirectsMiddleware:
    def __init__(self, get_response, resolver=None):
        self.get_response = get_response
        self.resolver = resolver or get_resolver()

    def __call__(self, request):
        response = self.process_request(request)
        if response:
            return response
        return self.get_response(request)

    def _drop_unsupported_locale_prefix(self, request):
        """Remove a leading product locale that Bedrock doesn't serve, if there is one.

        These redirects are resolved before `BedrockLangCodeFixupMiddleware` can fix the
        language codes up, so an off-site redirect (e.g. the release-notes pages that
        now live on www.firefox.com) would otherwise keep the unsupported prefix in its
        destination.
        """
        lang_code, subpath, lang_code_changed = split_path_and_normalize_language(request.path)
        if lang_code_changed and not lang_code:
            request.path = request.path_info = "/" + subpath

    def process_request(self, request):
        self._drop_unsupported_locale_prefix(request)
        try:
            resolver_match = self.resolver.resolve(request.path_info)
        except Resolver404:
            return None
        callback, callback_args, callback_kwargs = resolver_match
        request.resolver_match = resolver_match
        return callback(request, *callback_args, **callback_kwargs)
