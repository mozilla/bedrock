# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Custom Wagtail URL configuration that replaces the catch-all serve view.

Wagtail's default urls.py registers a catch-all regex that routes all
remaining page-like paths to ``wagtail.views.serve``.  This module keeps
Wagtail's utility URL patterns (password-protected page auth, frontend
login) but swaps the catch-all with our own view that handles alias-locale
fallback *before* deferring to Wagtail's serve.

Because this lives in the URL router, it only runs for paths that no other
Django view (including ``prefer_cms``-decorated views) has claimed.
"""

import logging

from django.urls import re_path

from wagtail.coreutils import WAGTAIL_APPEND_SLASH
from wagtail.urls import urlpatterns as _wagtail_urlpatterns

from bedrock.cms.views import wagtail_serve_with_locale_fallback

logger = logging.getLogger(__name__)

if WAGTAIL_APPEND_SLASH:
    _serve_pattern = r"^((?:[\w\-]+/)*)$"
else:
    _serve_pattern = r"^([\w\-/]*)$"

# Keep all Wagtail utility patterns; replace only the catch-all serve view.
urlpatterns = [p for p in _wagtail_urlpatterns if getattr(p, "name", None) != "wagtail_serve"]

_removed_count = len(_wagtail_urlpatterns) - len(urlpatterns)
if _removed_count != 1:
    logger.error(
        "Expected to remove exactly 1 pattern ('wagtail_serve') from Wagtail's urlpatterns, but removed %d. Wagtail patterns: %r",
        _removed_count,
        _wagtail_urlpatterns,
    )

urlpatterns.append(
    re_path(_serve_pattern, wagtail_serve_with_locale_fallback, name="wagtail_serve"),
)
