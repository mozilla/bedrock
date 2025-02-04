# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""URL paths which must be prefixed with a language code.

These are included in the main URLConf via the regular `patterns` function,
which will mean they are NOT prefixed with a language code.

Note that these are derived from the list of SUPPORTED_NONLOCALES and
SUPPORTED_LOCALE_IGNORE that were used in our former i18n machinery, and
which (currently) remain in use, so these two sources need to be kept in
sync with the urlpatterns below

Also, redirects from mozorg.urls were moved into here, so that they
don't get miss a lookup if they lack a locale code at the start of their path
"""

from django.urls import path

from bedrock.base import views

urlpatterns = (
    path("robots.txt", views.Robots.as_view(), name="robots.txt"),
    path(".well-known/security.txt", views.SecurityDotTxt.as_view(), name="security.txt"),
    path(".well-known/gpc.json", views.GpcDotJson.as_view(), name="gpc.json"),
    path("locales/", views.locales, name="mozorg.locales"),
)
