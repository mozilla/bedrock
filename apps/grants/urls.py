from django.conf.urls.defaults import patterns, url, include
import views
from mozorg.util import page

urlpatterns = patterns('',
    url('^$', views.index, name='grants.index'),
    url('list/', views.list, name='grants.list'),
    url('(?P<slug>[\w-]+)/', views.single, name='grants.single'),
)
