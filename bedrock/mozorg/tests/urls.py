# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path

from bedrock.mozorg.util import page


def mock_view(request):
    return HttpResponse("test")


urlpatterns = [
    path("", include(f"{settings.PROJECT_MODULE}.urls")),
    # Used by test_helper
    page("base/", "base-protocol.html"),
]
