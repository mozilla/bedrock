from django.conf.urls.defaults import *
from django.conf import settings
from product_details import product_details

from mozorg.util import page
import views

urlpatterns = patterns('',
    page('firefox/central', 'firefox/central.html'),
    page('firefox/channel', 'firefox/channel.html'),
    page('firefox/customize', 'firefox/customize.html'),
    page('firefox/features', 'firefox/features.html'),
    page('firefox/fx', 'firefox/fx.html'),
    page('firefox/geolocation', 'firefox/geolocation.html',
         gmap_api_key=settings.GMAP_API_KEY),
    page('firefox/happy', 'firefox/happy.html'),
    page('firefox/new', 'firefox/new.html'),
    page('firefox/organizations/faq', 'firefox/organizations/faq.html'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/performance', 'firefox/performance.html'),
    page('firefox/security', 'firefox/security.html'),
    page('firefox/speed', 'firefox/speed.html',
         latest_version=product_details.versions['LATEST_FIREFOX_DEVEL_VERSION']),
    page('firefox/technology', 'firefox/technology.html'),
    page('firefox/update', 'firefox/update.html'),

    page('firefox/unsupported/warning', 'firefox/unsupported-warning.html'),
    page('firefox/unsupported/EOL', 'firefox/unsupported-EOL.html'),

    url(r'^firefox/unsupported/win$', views.windows_billboards),
    url('^dnt/$', views.dnt, name='firefox.dnt'),
)
