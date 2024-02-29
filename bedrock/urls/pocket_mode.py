# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.urls import include, path
from django.utils.module_loading import import_string

from watchman import views as watchman_views

from bedrock.base import views as base_views
from bedrock.base.i18n import bedrock_i18n_patterns

# The default django 404 and 500 handler doesn't run the ContextProcessors,
# which breaks the base template page. So we replace them with views that do!
handler500 = "bedrock.pocket.views.server_error_view"
handler404 = "bedrock.pocket.views.page_not_found_view"

urlpatterns = bedrock_i18n_patterns(
    path("", include("bedrock.pocket.urls")),
)

urlpatterns += (
    path("healthz/", watchman_views.ping, name="watchman.ping"),
    path("readiness/", watchman_views.status, name="watchman.status"),
    path("healthz-cron/", base_views.cron_health_check),
)

if settings.DEBUG:
    urlpatterns += bedrock_i18n_patterns(
        path("404/", import_string(handler404)),
        path("500/", import_string(handler500)),
    )
