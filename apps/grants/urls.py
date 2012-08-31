from django.conf.urls.defaults import *
from mozorg.util import page

import views


urlpatterns = patterns('',
    url(r'^$', views.grants, name='grants'),
    # attempt to not break existing URL
    url(r'^(?P<slug>[\w-]+).html$', views.grant_info, name='grant_info'),
    # hard-code in a couple of static pages pulled direct from the old PHP site
    page('reports/gnome-haeger-report', 'grants/reports/gnome-haeger-report.html'),
    page('reports/ushahidi-chile-report', 'grants/reports/ushahidi-chile-report.html'),
)
