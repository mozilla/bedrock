# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from bedrock.mozorg.decorators import cache_control_expires
from bedrock.sitemaps.models import NO_LOCALE, SitemapURL


@method_decorator(cache_control_expires(1), name="dispatch")
class SitemapView(TemplateView):
    content_type = "text/xml"

    def _get_locale(self):
        if "is_none" in self.kwargs:
            # is_none here refers to the sitemap_none.xml URL. the value of that kwarg
            # when on that URL will be "_none" and will be None if not on that URL.
            # For that page we set the locale to the special value as that is what the entries
            # in the DB have recorded for locale for URLs that don't have a locale.
            locale = NO_LOCALE
        else:
            # can come back as empty string
            # should be None here if not a real locale because
            # None will mean that we should show the index of sitemaps
            # instead of a sitemap for a locale.
            locale = getattr(self.request, "locale", None)

        return locale

    def get_template_names(self):
        if self._get_locale():
            return ["sitemap.xml"]
        else:
            return ["sitemap_index.xml"]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        locale = self._get_locale()
        if locale:
            ctx["paths"] = SitemapURL.objects.all_for_locale(locale)
        else:
            ctx["locales"] = SitemapURL.objects.all_locales()
            ctx["NO_LOCALE"] = NO_LOCALE

        return ctx
