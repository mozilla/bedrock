# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.conf.urls import include, url
from django.http import HttpResponse

from bedrock.mozorg.util import page


def mock_view(request):
    return HttpResponse('test')

urlpatterns = (
    url(r'', include('%s.urls' % settings.PROJECT_MODULE)),

    # Used by test_helper
    page('base', 'base-resp.html'),
)
