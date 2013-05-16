# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *  # noqa
from django.conf import settings

from bedrock.firefox import version_re
from bedrock.redirects.util import redirect
from bedrock.mozorg.util import page
import views


latest_re = r'^firefox(?:/(%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')

# firstrun testing
# allow any (or no) string for version number
# currently want to restrict to 21.0 only, but
# left here for possible future use
# remove when firstrun experiment is over
#latest_new_re = r'^firefox(?:/(%s))?/firstrun/(?P<view>[a|b])(?P<version>[1-6])/$'
#firstrun_new_re = latest_new_re % version_re


urlpatterns = patterns('',
    url(r'^firefox/all/$', views.all_downloads, name='firefox.all'),
    page('firefox/central', 'firefox/central.html'),
    page('firefox/channel', 'firefox/channel.html'),
    redirect('^firefox/channel/android/$', 'firefox.channel'),
    page('firefox/customize', 'firefox/customize.html'),
    page('firefox/features', 'firefox/features.html'),
    page('firefox/fx', 'firefox/fx.html'),
    page('firefox/geolocation', 'firefox/geolocation.html',
         gmap_api_key=settings.GMAP_API_KEY),
    page('firefox/happy', 'firefox/happy.html'),
    page('firefox/memory', 'firefox/memory.html'),
    url('^firefox/mobile/platforms/$', views.platforms,
        name='firefox.mobile.platforms'),
    page('firefox/mobile/features', 'firefox/mobile/features.html'),
    page('firefox/mobile/faq', 'firefox/mobile/faq.html'),
    url('^firefox/sms/$', views.sms_send, name='firefox.sms'),
    page('firefox/sms/sent', 'firefox/mobile/sms-thankyou.html'),
    page('firefox/new', 'firefox/new.html'),
    page('firefox/organizations/faq', 'firefox/organizations/faq.html'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/performance', 'firefox/performance.html'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    page('firefox/security', 'firefox/security.html'),
    url(r'^firefox/installer-help/$', views.installer_help,
        name='firefox.installer-help'),
    page('firefox/speed', 'firefox/speed.html'),
    page('firefox/technology', 'firefox/technology.html'),
    page('firefox/toolkit/download-to-your-devices', 'firefox/devices.html'),
    page('firefox/update', 'firefox/update.html'),

    page('firefox/unsupported/warning', 'firefox/unsupported-warning.html'),
    page('firefox/unsupported/EOL', 'firefox/unsupported-EOL.html'),
    page('firefox/unsupported/mac', 'firefox/unsupported-mac.html'),

    url(r'^firefox/unsupported/win/$', views.windows_billboards),
    url('^dnt/$', views.dnt, name='firefox.dnt'),
    url(firstrun_re, views.latest_fx_redirect, name='firefox.firstrun',
        kwargs={'template_name': 'firefox/firstrun.html'}),
    url(whatsnew_re, views.latest_fx_redirect, name='firefox.whatsnew',
        kwargs={'template_name': 'firefox/whatsnew.html'}),
    # firstrun tests. remove when experiment is over
    url('^firefox/21.0/firstrun/(?P<view>[a|b])(?P<version>[1-6])/$', views.firstrun_new, name='firefox.firstrun.new'),

    url(r'^firefox/partners/$', views.firefox_partners,
        name='firefox.partners.index'),
)
