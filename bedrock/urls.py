# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import handler404
from django.urls import include, re_path

from django.utils.module_loading import import_string

from bedrock.base import views as base_views
from watchman import views as watchman_views

# The default django 500 handler doesn't run the ContextProcessors, which breaks
# the base template page. So we replace it with one that does!
handler500 = 'bedrock.base.views.server_error_view'


urlpatterns = (
    # Main pages
    re_path(r'^foundation/', include('bedrock.foundation.urls')),
    re_path(r'^grants/', include('bedrock.grants.urls')),
    re_path(r'^about/legal/', include('bedrock.legal.urls')),
    re_path(r'^press/', include('bedrock.press.urls')),
    re_path(r'^privacy/', include('bedrock.privacy.urls')),
    re_path(r'^styleguide/', include('bedrock.styleguide.urls')),
    re_path(r'^security/', include('bedrock.security.urls')),
    re_path(r'', include('bedrock.firefox.urls')),
    re_path(r'', include('bedrock.mozorg.urls')),
    re_path(r'', include('bedrock.newsletter.urls')),
    re_path(r'^etc/', include('bedrock.etc.urls')),
    re_path(r'^exp/', include('bedrock.exp.urls')),

    re_path(r'^healthz/$', watchman_views.ping, name="watchman.ping"),
    re_path(r'^readiness/$', watchman_views.status, name="watchman.status"),
    re_path(r'^healthz-cron/$', base_views.cron_health_check),
    re_path(r'^csp-violation-capture$', base_views.csp_violation_capture,
        name='csp-violation-capture'),
    re_path(r'^country-code\.json$', base_views.geolocate,
        name='geolocate')
)

if settings.DEBUG:

    def show404(request):
        return import_string(handler404)(request, '')

    urlpatterns += (
        re_path(r'^404/$', show404),
        re_path(r'^500/$', import_string(handler500)),
    )
