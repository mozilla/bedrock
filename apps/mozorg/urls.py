from django.conf.urls.defaults import *
from generics.views import page

urlpatterns = patterns('',
    page("", "mozorg/home.html"),

    page('about', 'mozorg/about.html'),
    page('projects', 'mozorg/projects.html'),
    page('button', 'mozorg/button.html'),
    page('sandstone', 'mozorg/sandstone.html'),
    page('contribute', 'mozorg/contribute.html'),
    page('mission', 'mozorg/mission.html'),
)
