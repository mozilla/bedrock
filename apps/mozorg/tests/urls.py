from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse

from mozorg.util import redirect


def mock_view(request):
    return HttpResponse('test')

urlpatterns = patterns('',
    url(r'^mock/view/$', mock_view, name='mock_view'),
    redirect(r'^gloubi-boulga/$', 'mock_view'),
    redirect(r'^gloubi-boulga/tmp/$', 'mock_view', permanent=False),
)
