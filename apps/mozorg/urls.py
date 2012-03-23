from django.conf.urls.defaults import *
from generics.views import page
from views import channel

urlpatterns = patterns('',
    page("", "mozorg/home.html"),

    page("button", "mozorg/button.html"),
    page("sandstone", "mozorg/sandstone.html"),
    page("contribute", "mozorg/contribute.html"),
    page("mission", "mozorg/mission.html"),

    url(r'^channel/$', channel, name='mozorg.channel'),
)
