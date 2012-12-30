# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
from django.conf.urls.defaults import include, patterns
from django.http import HttpResponse

from funfactory.manage import ROOT

from mozorg.util import page


def mock_view(request):
    return HttpResponse('test')

urlpatterns = patterns('',
    (r'', include('%s.urls' % os.path.basename(ROOT))),

    # Used by test_helper
    page('base', 'base-resp.html'),
)
