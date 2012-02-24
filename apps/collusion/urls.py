from django.conf.urls.defaults import *
from views import collusion, demo

urlpatterns = patterns('',
    (r'^demo/$', demo),
    (r'^$', collusion),
)
