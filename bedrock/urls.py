#!/usr/bin/python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import handler404
from django.urls import include, path

from django.utils.module_loading import import_string

from bedrock.base import views as base_views
from watchman import views as watchman_views

# The default django 500 handler doesn't run the ContextProcessors, which breaks
# the base template page. So we replace it with one that does!

handler500 = 'bedrock.base.views.server_error_view'

urlpatterns = (  # Main pages
    path('foundation/', include('bedrock.foundation.urls')),
    path('grants/', include('bedrock.grants.urls')),
    path('about/legal/', include('bedrock.legal.urls')),
    path('press/', include('bedrock.press.urls')),
    path('privacy/', include('bedrock.privacy.urls')),
    path('styleguide/', include('bedrock.styleguide.urls')),
    path('security/', include('bedrock.security.urls')),
    path('', include('bedrock.firefox.urls')),
    path('', include('bedrock.mozorg.urls')),
    path('', include('bedrock.newsletter.urls')),
    path('etc/', include('bedrock.etc.urls')),
    path('exp/', include('bedrock.exp.urls')),
    path('healthz/', watchman_views.ping, name='watchman.ping'),
    path('readiness/', watchman_views.status, name='watchman.status'),
    path('healthz-cron/', base_views.cron_health_check),
    path('csp-violation-capture', base_views.csp_violation_capture,
         name='csp-violation-capture'),
    path('country-code.json', base_views.geolocate, name='geolocate'),
    )

if settings.DEBUG:


    def show404(request):
        return import_string(handler404)(request, '')


    urlpatterns += (path('404/', show404), path('500/',
    urlpatterns += (
        path('404/', show404), 
        path('500/', import_string(handler500)),
    )
