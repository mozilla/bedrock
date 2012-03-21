from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='mozorg.home'),

    url(r'^button/$', views.button),
    url(r'^channel/$', views.channel),
    url(r'^sandstone/', views.sandstone),
    url(r'^contribute/$', views.contribute, name='mozorg.contribute'),
    url(r'^mission/$', views.mission, name='mozorg.mission'),
)
