# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# URL Patterns for www.mozilla.org

from django.urls import include, path


urlpatterns = [
    # Main pages
    path('foundation/', include('bedrock.foundation.urls')),
    path('grants/', include('bedrock.grants.urls')),
    path('about/legal/', include('bedrock.legal.urls')),
    path('press/', include('bedrock.press.urls')),
    path('privacy/', include('bedrock.privacy.urls')),
    path('styleguide/', include('bedrock.styleguide.urls')),
    path('security/', include('bedrock.security.urls')),
    path('firefox/', include('bedrock.firefox.urls')),
    path('etc/', include('bedrock.etc.urls')),
    path('exp/', include('bedrock.exp.urls')),
    path('', include('bedrock.mozorg.urls')),
    path('', include('bedrock.newsletter.urls')),
]
