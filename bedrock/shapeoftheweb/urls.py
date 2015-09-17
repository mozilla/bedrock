# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

from bedrock.shapeoftheweb import views


urlpatterns = (
    url(r'^(?P<filename>(?:main|country-data|infographics)\.json)$', views.localized_json,
        name='shapeoftheweb.localized_json'),
)
