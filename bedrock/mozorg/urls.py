# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from util import page
import views

urlpatterns = patterns('',
    page("", "mozorg/home.html"),
    page('about/manifesto', 'mozorg/about/manifesto.html'),
    page('about', 'mozorg/about.html'),
    page('book', 'mozorg/book.html'),
    url('^about/partnerships/$', views.partnerships, name='mozorg.partnerships'),
    page('about/partnerships/distribution', 'mozorg/partnerships-distribution.html'),
    page('about/history', 'mozorg/about/history.html'),
    page('products', 'mozorg/products.html'),
    page('about/mozilla-based', 'mozorg/projects/mozilla-based.html'),
    page('button', 'mozorg/button.html'),
    page('mission', 'mozorg/mission.html'),
    page('mobile', 'mozorg/mobile.html'),
    page('ITU', 'mozorg/itu.html'),
    page('about/powered-by', 'mozorg/powered-by.html'),

    url('^newsletter/hacks\.mozilla\.org/$', views.hacks_newsletter,
        name='mozorg.hacks_newsletter'),
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
    url('^contribute/embed/$', views.contribute_embed,
        name='mozorg.contribute_embed',
        kwargs={'template': 'mozorg/contribute-embed.html',
                'return_to_form': False}),
    url('^contribute/universityambassadors/$',
        views.contribute_university_ambassadors,
        name='mozorg.contribute_university_ambassadors'),
    page('contribute/universityambassadors/thanks',
         'mozorg/contribute_university_ambassadors_thanks.html'),
    url(r'^about/partnerships/contact-bizdev/$', views.contact_bizdev,
        name='about.partnerships.contact-bizdev'),
    url(r'^plugincheck/$',
        views.plugincheck,
        name='mozorg.plugincheck'),
)
