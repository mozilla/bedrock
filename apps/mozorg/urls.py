from django.conf.urls.defaults import *
from util import page, redirect
import views

urlpatterns = patterns('',
    page("", "mozorg/home.html"),

    page('about', 'mozorg/about.html'),
    page('about/partnerships', 'mozorg/partnerships.html'),
    page('about/partnerships/distribution', 'mozorg/partnerships-distribution.html'),
    page('products', 'mozorg/products.html'),
    page('projects/mozilla-based', 'mozorg/projects/mozilla-based.html'),
    page('button', 'mozorg/button.html'),
    page('sandstone', 'mozorg/sandstone.html'),
    page('mission', 'mozorg/mission.html'),
    page('mobile', 'mozorg/mobile.html'),

    url('^contribute/$', views.contribute, name='mozorg.contribute'),
    url('^contribute/page/$', views.contribute,
        {'template': 'mozorg/contribute-page.html'},
        name='mozorg.contribute_page'),
    redirect(r'^projects/$', 'mozorg.products'),
)
