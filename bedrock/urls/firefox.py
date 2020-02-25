# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# URL Patterns for www.mozilla.org

from django.urls import include, path


urlpatterns = [
    # Main pages
    path('', include('bedrock.firefox.urls')),

    # mostly here for now to fix missing url patterns.
    # we'll change those to redirect definitions later if we go this route.
    path('', include('bedrock.mozorg.urls')),
    path('', include('bedrock.newsletter.urls')),
    path('about/legal/', include('bedrock.legal.urls')),
    path('privacy/', include('bedrock.privacy.urls')),
    path('foundation/', include('bedrock.foundation.urls')),
    path('grants/', include('bedrock.grants.urls')),
    path('security/', include('bedrock.security.urls')),
    path('etc/', include('bedrock.etc.urls')),
    path('exp/', include('bedrock.exp.urls')),
]
