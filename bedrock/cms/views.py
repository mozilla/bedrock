# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import Http404, HttpResponseRedirect

from wagtail.models import Locale as WagtailLocale, Site
from wagtail.views import serve as wagtail_serve

from bedrock.cms.utils import find_fallback_page_for_locale


def _alias_needs_prewagtail_intercept(lang_prefix):
    """
    Return True if the alias locale requires interception before Wagtail handles the request:

        1. If lang_prefix is not a configured alias locale, we do not intercept.
        2. Otherwise, pre-Wagtail interception is needed when Wagtail cannot correctly
           serve pages for this alias locale on its own. Either of these:
           a. No Locale DB record exists, OR
           b. The Locale record exists but site.root_page has no live translation in this locale.
    Wagtail's default behaviour would serve the en-US homepage, which is not
    what we want for alias locales.
    """
    fallback_locales = getattr(settings, "FALLBACK_LOCALES", {})
    if lang_prefix not in fallback_locales:
        return False

    alias_locale = WagtailLocale.objects.filter(language_code=lang_prefix).first()
    if not alias_locale:
        return True

    site = Site.objects.filter(is_default_site=True).select_related("root_page").first()
    if not site:
        return False

    alias_root = site.root_page.get_translation_or_none(alias_locale)
    return not alias_root or not alias_root.live


def _serve_fallback_page(request, lang_prefix, sub_path, fallback_locales):
    """
    Find and serve the fallback locale's page for an alias locale URL.

    Returns an HttpResponse if a fallback page is found, or None if no fallback
    page exists (allowing the caller to fall through to other checks).

    View-restricted pages are never transparently served; they redirect to the
    canonical URL so Wagtail's restriction enforcement fires there.
    """
    fallback_page = find_fallback_page_for_locale(lang_prefix, sub_path)
    if not fallback_page:
        return None

    if fallback_page.get_view_restrictions():
        return HttpResponseRedirect(fallback_page.url)

    specific_page = fallback_page.specific
    request.content_locale = fallback_locales[lang_prefix]
    # Note: we intentionally do NOT call translation.activate(request.content_locale)
    # here, even though it would make BedrockLocale.get_active() resolve to the
    # fallback locale's Wagtail Locale object.
    # The reason: Django's LocalePrefixPattern.language_prefix reads
    # translation.get_language() directly, so activating a different locale
    # (e.g. pt-BR while serving /pt-PT/) would cause all url() template calls
    # to generate links with the wrong locale prefix.
    # Setting request.content_locale carries the fallback locale into the render
    # pipeline without disturbing URL generation.
    return specific_page.serve(request)


def wagtail_serve_with_locale_fallback(request, path=""):
    """
    Wagtail serve wrapper that handles alias-locale fallback.

    This can be used both as the Wagtail catch-all URL pattern (replacing
    ``wagtail.views.serve``) and by ``prefer_cms`` (replacing its direct
    ``wagtail_serve`` call).

    For alias locales that Wagtail cannot serve correctly on its own
    (no Locale DB record, or no live root page translation), this view
    tries to serve the fallback locale's page before deferring to Wagtail.

    For alias locales with a live root page in Wagtail, but no page at the specific
    path (Wagtail would Http404), the fallback locale's page is also tried.

    If no fallback page exists either, raises Http404 so that callers
    (prefer_cms, middleware) can apply their own fallback logic.
    """
    _path = request.path.lstrip("/")
    lang_prefix, _, sub_path = _path.partition("/")
    fallback_locales = getattr(settings, "FALLBACK_LOCALES", {})

    if _alias_needs_prewagtail_intercept(lang_prefix):
        response = _serve_fallback_page(request, lang_prefix, sub_path, fallback_locales)
        if response is not None:
            return response
        # No fallback page and Wagtail can't serve this alias locale
        # correctly — raise 404 so:
        #  - prefer_cms can fall through to its Django view
        #  - CMSLocaleFallbackMiddleware can try the Accept-Language redirect
        raise Http404

    # Try to serve the response with Wagtail, but if Wagtail gives us a 404 for
    # an alias locale, then we try to serve the fallback page.
    # If we can't serve the fallback page, then keep Wagtail's 404, so:
    #    - prefer_cms can fall through to its Django view
    #    - CMSLocaleFallbackMiddleware can try the Accept-Language redirect
    try:
        wagtail_response = wagtail_serve(request, path)
    except Http404:
        if lang_prefix in fallback_locales:
            response = _serve_fallback_page(request, lang_prefix, sub_path, fallback_locales)
            if response is not None:
                return response
        raise
    return wagtail_response
