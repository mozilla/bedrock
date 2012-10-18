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
