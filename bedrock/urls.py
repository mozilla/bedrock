# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.utils.module_loading import import_string

import wagtaildraftsharing.urls as wagtaildraftsharing_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from watchman import views as watchman_views

from bedrock.base import views as base_views
from bedrock.base.i18n import bedrock_i18n_patterns
from bedrock.cms.bedrock_wagtail_urls import custom_wagtail_urls

# The default django 404 and 500 handler doesn't run the ContextProcessors,
# which breaks the base template page. So we replace them with views that do!
handler500 = "bedrock.base.views.server_error_view"
handler404 = "bedrock.base.views.page_not_found_view"
locale404 = "lib.l10n_utils.locale_selection"

# Paths that should have a locale prefix
urlpatterns = bedrock_i18n_patterns(
    # Main pages
    path("foundation/", include("bedrock.foundation.urls")),
    path("about/legal/", include("bedrock.legal.urls")),
    path("press/", include("bedrock.press.urls")),
    path("privacy/", include("bedrock.privacy.urls")),
    path("products/", include("bedrock.products.urls")),
    path("security/", include("bedrock.security.urls")),
    path("", include("bedrock.firefox.urls")),
    path("", include("bedrock.mozorg.urls")),  # these are locale-needing URLs, vs mozorg.nonlocale_urls
    path("", include("bedrock.newsletter.urls")),
    path("careers/", include("bedrock.careers.urls")),
)

# Paths that must not have a locale prefix
urlpatterns += (
    path("", include("bedrock.mozorg.nonlocale_urls")),
    path("", include("bedrock.sitemaps.urls")),
    path("healthz/", watchman_views.ping, name="watchman.ping"),
    path("readiness/", watchman_views.status, name="watchman.status"),
    path("healthz-cron/", base_views.cron_health_check),
    path("_documents/", include(wagtaildocs_urls)),
)

if settings.DEV:
    urlpatterns += bedrock_i18n_patterns(
        # Add /404-locale/ for localizers.
        path("404-locale/", import_string(locale404)),
    )

if settings.DEBUG:
    urlpatterns += bedrock_i18n_patterns(
        path("404/", import_string(handler404)),
        path("500/", import_string(handler500)),
    )
    urlpatterns += (path("csrf_403/", base_views.csrf_failure, {}),)

if settings.WAGTAIL_ENABLE_ADMIN:
    # If adding new a new path here, you must also add an entry to
    # settings.SUPPORTED_NONLOCALES in the `if WAGTAIL_ENABLE_ADMIN` block so
    # that bedrock doesn't try to prepend a locale onto requests for the path
    urlpatterns += (
        path("oidc/", include("mozilla_django_oidc.urls")),
        path("cms-admin/", include(wagtailadmin_urls)),
        path("django-admin/", admin.site.urls),  # needed to show django-rq UI
        path("django-rq/", include("django_rq.urls")),  # task queue management
        path("_internal_draft_preview/", include(wagtaildraftsharing_urls)),  # ONLY available in CMS mode
    )

if settings.ENABLE_DJANGO_SILK:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

if settings.DEFAULT_FILE_STORAGE == "django.core.files.storage.FileSystemStorage":
    # Serve media files from Django itself - production won't use this
    from django.urls import re_path
    from django.views.static import serve

    urlpatterns += (
        re_path(
            r"^custom-media/(?P<path>.*)$",
            serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
    )
    # Note that statics are handled via Whitenoise's middleware

# Wagtail is the catch-all route, and it will raise a 404 if needed.
# We have customised wagtail_urls in order to decorate wagtail_serve
# to 'get ahead' of that 404 raising, to avoid hitting the database.
urlpatterns += bedrock_i18n_patterns(
    path("", include(custom_wagtail_urls)),
)
