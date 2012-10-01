from django.conf.urls.defaults import *
from django.conf import settings
from product_details import product_details

from firefox import version_re
from mozorg.util import page, redirect
import views

whatsnew_re = r'^firefox(?:/(%s))?/whatsnew/$' % version_re

urlpatterns = patterns('',
    page('firefox/central', 'firefox/central.html'),
    page('firefox/channel', 'firefox/channel.html'),
    redirect('^firefox/channel/android/$', 'firefox.channel'),
    page('firefox/customize', 'firefox/customize.html'),
    page('firefox/features', 'firefox/features.html'),
    page('firefox/fx', 'firefox/fx.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION']),
    page('firefox/geolocation', 'firefox/geolocation.html',
         gmap_api_key=settings.GMAP_API_KEY),
    page('firefox/happy', 'firefox/happy.html'),
    page('firefox/memory', 'firefox/memory.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION']),
    url('^firefox/mobile/platforms/$', views.platforms, name='firefox.mobile.platforms'),
    page('firefox/mobile/features', 'firefox/mobile/features.html'),
    page('firefox/mobile/faq', 'firefox/mobile/faq.html'),
    url('^firefox/sms/$', views.sms_send, name='firefox.sms'),
    page('firefox/sms-sent', 'firefox/mobile/sms-thankyou.html'),
    page('firefox/new', 'firefox/new.html'),
    page('firefox/organizations/faq', 'firefox/organizations/faq.html'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/performance', 'firefox/performance.html'),
    page('firefox/security', 'firefox/security.html'),
    page('firefox/installer-help', 'firefox/installer-help.html'),
    page('firefox/speed', 'firefox/speed.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION']),
    page('firefox/technology', 'firefox/technology.html'),
    page('firefox/toolkit/download-to-your-devices', 'firefox/devices.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION']),
    page('firefox/update', 'firefox/update.html',
         latest_version=product_details.firefox_versions['LATEST_FIREFOX_VERSION']),

    page('firefox/unsupported/warning', 'firefox/unsupported-warning.html'),
    page('firefox/unsupported/EOL', 'firefox/unsupported-EOL.html'),

    url(r'^firefox/unsupported/win/$', views.windows_billboards),
    url('^dnt/$', views.dnt, name='firefox.dnt'),
    url(whatsnew_re, views.whatsnew_redirect, name='firefox.whatsnew'),
)
