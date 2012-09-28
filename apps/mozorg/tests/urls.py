import os
from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponse

from funfactory.manage import ROOT

from redirects.util import redirect
from mozorg.util import page


def mock_view(request):
    return HttpResponse('test')

urlpatterns = patterns('',
    (r'', include('%s.urls' % os.path.basename(ROOT))),

    # Used by test_util
    url(r'^mock/view/$', mock_view, name='mock_view'),
    redirect(r'^gloubi-boulga/$', 'mock_view'),
    redirect(r'^gloubi-boulga/tmp/$', 'mock_view', permanent=False),

    # Used by test_helper
    page('base', 'base-resp.html'),
)
