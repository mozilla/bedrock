from django.conf.urls.defaults import *
from views import home, contribute, channel, button, sandstone, mission


urlpatterns = patterns('',
    url(r'^$', home, name='mozorg.home'),

    url(r'^button/$', button),
    url(r'^channel/$', channel),
    url(r'^sandstone/', sandstone),
    url(r'^contribute/$', contribute, name='mozorg.contribute'),
    url(r'^mission/$', mission, name='mozorg.mission'),
)
