# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.utils.cache import add_never_cache_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from wagtail.models import Page as WagtailBasePage

from lib import l10n_utils


@method_decorator(never_cache, name="serve_password_required_response")
class AbstractBedrockCMSPage(WagtailBasePage):
    """Base page class for all Wagtail pages within Bedrock

    Things we do to in particular are:

    * Use our l10n_utils.render() method so that templates can use Fluent string

    * Ensure private pages are not cached:
        By default, Wagtail is unopinionated about cache-control headers,
        so we need to be sure that pages with acecss restrictions are _not_
        cached anywhere in a shared resource (e.g. the CDN)
        Taking our lead from the relevant Wagtail issue
        https://github.com/wagtail/wagtail/issues/5072#issuecomment-949397013, we:
        1) Override the default `serve()` method with cache-control settings
        for pages with view restrictions.
        2) Apply `never_cache` headers to the `wagtail.Page` class's
        `serve_password_required_response` method, via the @method_decorator above
    """

    class Meta:
        abstract = True

    def _patch_request_for_bedrock(self, request):
        # Add hints that help us integrate CMS pages with core Bedrock logic
        request.is_cms_page = True
        request._locales_available_via_cms = [self.locale.language_code] + [x.locale.language_code for x in self.get_translations()]
        return request

    def _render_with_fluent_string_support(self, request, *args, **kwargs):
        # Normally, Wagtail's serve() returns a TemplateResponse, so we
        # can swap that for our Fluent-compatible rendering method
        template = self.get_template(request, *args, **kwargs)
        context = self.get_context(request, *args, **kwargs)
        # We shouldn't need to spec any special ftl_files param for render()
        # here because the global spec is in settings.FLUENT_DEFAULT_FILES
        return l10n_utils.render(request, template, context)

    def serve(self, request, *args, **kwargs):
        # Need to replicate behaviour in https://github.com/wagtail/wagtail/blob/stable/5.2.x/wagtail/models/__init__.py#L1928
        request.is_preview = False

        request = self._patch_request_for_bedrock(request)

        response = self._render_with_fluent_string_support(request, *args, **kwargs)

        if len(self.get_view_restrictions()):
            add_never_cache_headers(response)
        return response

    def serve_preview(self, request, *args, **kwargs):
        request = self._patch_request_for_bedrock(request)
        return self._render_with_fluent_string_support(request, *args, **kwargs)
