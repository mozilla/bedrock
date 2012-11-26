# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse

from redirects.util import redirect


def mock_view(request):
    return HttpResponse('test')

urlpatterns = patterns('',
    # Used by test_util
    url(r'^mock/view/$', mock_view, name='mock_view'),
    redirect(r'^gloubi-boulga/$', 'mock_view'),
    redirect(r'^gloubi-boulga/tmp/$', 'mock_view', permanent=False),
    redirect(r'^gloubi-boulga/ext/$', 'https://marketplace.mozilla.org'),
)
