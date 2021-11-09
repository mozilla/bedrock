# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# URLS only available with settings.DEV is enabled
from django.urls import path

from bedrock.mozorg import views

urlpatterns = (
    path(
        "contentful-preview/<content_id>/",
        views.ContentfulPreviewView.as_view(),
        name="contentful.preview",
    ),
)
