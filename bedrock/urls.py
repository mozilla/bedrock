# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import handler404, include, url


# The default django 500 handler doesn't run the ContextProcessors, which breaks
# the base template page. So we replace it with one that does!
handler500 = 'bedrock.base.views.server_error_view'


urlpatterns = (
    # Main pages
    url(r'^lightbeam/', include('bedrock.lightbeam.urls')),
    url(r'^foundation/', include('bedrock.foundation.urls')),
    url(r'^grants/', include('bedrock.grants.urls')),
    url(r'^infobar/', include('bedrock.infobar.urls')),
    url(r'^about/legal/', include('bedrock.legal.urls')),
    url(r'^press/', include('bedrock.press.urls')),
    url(r'^privacy', include('bedrock.privacy.urls')),
    url(r'^styleguide/', include('bedrock.styleguide.urls')),
    url(r'^tabzilla/', include('bedrock.tabzilla.urls')),
    url(r'^security/', include('bedrock.security.urls')),
    url(r'^shapeoftheweb/', include('bedrock.shapeoftheweb.urls')),
    url(r'', include('bedrock.firefox.urls')),
    url(r'', include('bedrock.thunderbird.urls')),
    url(r'', include('bedrock.mozorg.urls')),
    url(r'', include('bedrock.newsletter.urls')),
    url(r'', include('bedrock.teach.urls')),
    url(r'^etc/', include('bedrock.etc.urls')),

    # L10n example.
    url(r'^l10n_example/',
        include('bedrock.l10n_example.urls')),

    url(r'^healthz/$', 'bedrock.base.views.health_check'),
    url(r'^healthz-cron/$', 'bedrock.base.views.cron_health_check'),
    url(r'^csp-violation-capture$', 'bedrock.base.views.csp_violation_capture',
        name='csp-violation-capture'),
    url(r'^country-code\.json$', 'bedrock.base.views.geolocate',
        name='geolocate')
)

if settings.DEBUG:
    urlpatterns += (url(r'^404/$', handler404),
                    url(r'^500/$', handler500))
