from django.conf.urls.defaults import include, patterns, url
from django.http import HttpResponse

from mozorg.util import page, redirect


def mock_view(request):
    return HttpResponse('test')

urlpatterns = patterns('',
    (r'', include('bedrock.urls')),

    # Used by test_util
    url(r'^mock/view/$', mock_view, name='mock_view'),
    redirect(r'^gloubi-boulga/$', 'mock_view'),
    redirect(r'^gloubi-boulga/tmp/$', 'mock_view', permanent=False),

    # Used by test_helper
    page('base', 'base-resp.html'),
)
