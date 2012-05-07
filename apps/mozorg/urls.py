from django.conf.urls.defaults import *
from util import page
import views

urlpatterns = patterns('',
    page("", "mozorg/home.html"),

    page('about', 'mozorg/about.html'),
    page('about/partnerships', 'mozorg/partnerships.html'),
    page('about/partnerships/distribution', 'mozorg/partnerships-distribution.html'),
    page('projects', 'mozorg/projects.html'),
    page('button', 'mozorg/button.html'),
    page('sandstone', 'mozorg/sandstone.html'),
    page('mission', 'mozorg/mission.html'),

    url('^contribute/$', views.contribute, name='mozorg.contribute'),
    page('contribute/page', 'mozorg/contribute-page.html'),
)
