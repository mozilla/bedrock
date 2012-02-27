from django.conf.urls.defaults import *
from views import collusion, demo

urlpatterns = patterns('',
    url(r'^demo/$', demo, name='collusion.demo'),
    url(r'^$', collusion, name='collusion'),
)
