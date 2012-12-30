# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from redirects.util import redirect
from util import page
import views

urlpatterns = patterns('',
    page("", "mozorg/home.html"),

    page('about', 'mozorg/about.html'),
    page('book', 'mozorg/book.html'),
    page('about/partnerships', 'mozorg/partnerships.html'),
    page('about/partnerships/distribution', 'mozorg/partnerships-distribution.html'),
    page('products', 'mozorg/products.html'),
    page('projects/mozilla-based', 'mozorg/projects/mozilla-based.html'),
    page('button', 'mozorg/button.html'),
    page('sandstone', 'mozorg/sandstone.html'),
    page('mission', 'mozorg/mission.html'),
    page('mobile', 'mozorg/mobile.html'),
    page('ITU', 'mozorg/itu.html'),

    url('^contribute/$', views.contribute, name='mozorg.contribute',
        kwargs={'template': 'mozorg/contribute.html',
                'return_to_form': False}),
    url('^contribute/event/$', views.contribute,
        kwargs={'template': 'mozorg/contribute.html',
                'return_to_form': True},
        name='mozorg.contribute_event'),
    url('^contribute/page/$', views.contribute,
        kwargs={'template': 'mozorg/contribute-page.html',
                'return_to_form': False},
        name='mozorg.contribute_page'),

)
