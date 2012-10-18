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
