# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

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
    url('^contribute/page/$', views.contribute_page, name='mozorg.contribute_page'),
)
