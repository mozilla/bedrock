# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# URLS only available with settings.DEV is enabled
from django.urls import path

from bedrock.base.i18n import bedrock_i18n_patterns
from bedrock.mozorg import views

urlpatterns = bedrock_i18n_patterns(
    path(
        "contentful-preview/<content_id>/",
        views.ContentfulPreviewView.as_view(),
        name="contentful.preview",
    ),
)
