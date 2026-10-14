# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.http import HttpResponse
from django.urls import path, re_path

from bedrock.base.i18n import bedrock_i18n_patterns
from lib import l10n_utils


def translated(locales):
    # get_static_urls() only needs the render context
    def view(request, **kwargs):
        return l10n_utils.django_render(request, "sitemap-test.html", {"translations": dict.fromkeys(locales, "")})

    return view


def no_translations(request):
    # renders without translations
    return l10n_utils.django_render(request, "sitemap-test.html", {})


def no_render(request):
    return HttpResponse("not rendered through l10n_utils")


# URLs for testing get_static_urls()
urlpatterns = [
    path("credits/", no_render, name="credits"),
    path("robots.txt", no_render, name="robots"),
    path("healthz/", no_render, name="healthz"),
    re_path(r"^media/(?P<path>.*)$", no_render, name="media"),
]

urlpatterns += bedrock_i18n_patterns(
    path("translated/", translated(["en-US", "de", "fr", "zz"]), name="translated"),
    path("privacy/firefox-focus/", translated(["en-US", "de", "fr"]), name="firefox-focus"),
    path("extra/", translated(["en-US", "fr"]), name="extra"),
    path("detail/<slug:slug>/", translated(["en-US"]), name="detail"),
    path("firefox/welcome/1/", translated(["en-US"]), name="noindex"),
    path("no-translations/", no_translations, name="no-translations"),
    path("no-render/", no_render, name="no-render"),
)
