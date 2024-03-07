# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""URL paths which must be prefixed with a language code.

These are included in the main URLConf via the regular `patterns` function,
which will mean they are NOT prefixed with a language code.

Note that these were derived from the list of SUPPORTED_NONLOCALES and
SUPPORTED_LOCALE_IGNORE that were used in our former i18n machinery.

Also, redirects from mozorg.urls were moved into here, so that they
don't get miss a lookup if they lack a locale code at the start of their path
"""


from django.conf import settings
from django.urls import path

from . import views
from .dev_urls import urlpatterns as dev_only_urlpatterns
from .util import page

urlpatterns = (
    path("credits/", views.credits_view, name="mozorg.credits"),
    page("credits/faq/", "mozorg/credits-faq.html"),
    path("robots.txt", views.Robots.as_view(), name="robots.txt"),
    path(".well-known/security.txt", views.SecurityDotTxt.as_view(), name="security.txt"),
    # namespaces
    path("2004/em-rdf", views.namespaces, {"namespace": "em-rdf"}),
    path("2005/app-update", views.namespaces, {"namespace": "update"}),
    path("2006/addons-blocklist", views.namespaces, {"namespace": "addons-bl"}),
    path("2006/browser/search/", views.namespaces, {"namespace": "mozsearch"}),
    path("keymaster/gatekeeper/there.is.only.xul", views.namespaces, {"namespace": "xul"}),
    path("microsummaries/0.1", views.namespaces, {"namespace": "microsummaries"}),
    path("projects/xforms/2005/type", views.namespaces, {"namespace": "xforms-type"}),
    path("xbl", views.namespaces, {"namespace": "xbl"}),
    path("locales/", views.locales, name="mozorg.locales"),
)

if settings.DEV:
    urlpatterns += dev_only_urlpatterns
