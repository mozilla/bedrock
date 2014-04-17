# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import patterns, url

from bedrock.firefox import version_re
from bedrock.redirects.util import redirect
from bedrock.mozorg.util import page
import views


latest_re = r'^firefox(?:/(?P<fx_version>%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')
whatsnew_re_b = latest_re % (version_re, 'whatsnew/b')
tour_re = latest_re % (version_re, 'tour')
product_re = '(?P<product>firefox|mobile)'
channel_re = '(?P<channel>beta|aurora|organizations)'
releasenotes_re = latest_re % (version_re, r'(aurora|release)notes')
mobile_releasenotes_re = releasenotes_re.replace('firefox', 'mobile')
sysreq_re = latest_re % (version_re, 'system-requirements')


urlpatterns = patterns('',
    url('^(?:%s)/(?:%s/)?notes/$' % (product_re, channel_re),
        views.latest_notes, name='firefox.notes'),

    redirect(r'^firefox/$', 'firefox.new', name='firefox'),

    url(r'^firefox/(?:%s/)?all/$' % channel_re,
        views.all_downloads, name='firefox.all'),

    url('^dnt/$', views.dnt, name='firefox.dnt'),
    page('firefox/central', 'firefox/central.html'),
    page('firefox/channel', 'firefox/channel.html'),
    redirect('^firefox/channel/android/$', 'firefox.channel'),
    page('firefox/customize', 'firefox/customize.html'),
    page('firefox/desktop', 'firefox/desktop/index.html'),
    page('firefox/desktop/fast', 'firefox/desktop/fast.html'),
    page('firefox/desktop/customize', 'firefox/desktop/customize.html'),
    page('firefox/desktop/trust', 'firefox/desktop/trust.html'),
    page('firefox/features', 'firefox/features.html'),
    page('firefox/fx', 'firefox/fx.html'),
    page('firefox/geolocation', 'firefox/geolocation.html'),
    page('firefox/happy', 'firefox/happy.html'),

    url(r'^firefox/installer-help/$', views.installer_help,
        name='firefox.installer-help'),
    url('^firefox/latest/releasenotes/$', views.latest_notes),
    url('^firefox/(?:%s/)?system-requirements/$' % channel_re,
        views.latest_sysreq, name='firefox.sysreq'),
    page('firefox/memory', 'firefox/memory.html'),
    page('firefox/mobile/features', 'firefox/mobile/features.html'),
    page('firefox/mobile/faq', 'firefox/mobile/faq.html'),
    page('firefox/os/faq', 'firefox/os/faq.html'),
    url('^firefox/sms/$', views.sms_send, name='firefox.sms'),
    page('firefox/sms/sent', 'firefox/mobile/sms-thankyou.html'),
    page('firefox/sync', 'firefox/sync.html'),
    page('firefox/new', 'firefox/new.html'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    page('firefox/organizations/faq', 'firefox/organizations/faq.html'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/os', 'firefox/os/index.html'),
    page('firefox/os/devices', 'firefox/os/devices.html'),
    page('firefox/os/faq', 'firefox/os/faq.html'),
    # firefox/os/notes/ should redirect to the latest version; update this in /redirects/urls.py
    url('^firefox/os/notes/(?P<fx_version>%s)/$' % version_re,
        views.release_notes, {'product': 'Firefox OS'},
        name='firefox.os.releasenotes'),
    page('firefox/os/releases', 'firefox/os/releases.html'),
    url(r'^firefox/partners/$', views.firefox_partners,
        name='firefox.partners.index'),
    page('firefox/performance', 'firefox/performance.html'),
    url('^firefox/releases/$', views.releases_index,
        name='firefox.releases.index'),
    page('firefox/security', 'firefox/security.html'),
    url('^firefox/sms/$', views.sms_send, name='firefox.sms'),
    page('firefox/sms/sent', 'firefox/mobile/sms-thankyou.html'),
    page('firefox/speed', 'firefox/speed.html'),
    page('firefox/technology', 'firefox/technology.html'),
    page('firefox/unsupported/details', 'firefox/unsupported/details.html'),
    page('firefox/unsupported/EOL', 'firefox/unsupported/EOL.html'),
    page('firefox/unsupported/mac', 'firefox/unsupported/mac.html'),
    page('firefox/unsupported/warning', 'firefox/unsupported/warning.html'),
    url(r'^firefox/unsupported/win/$', views.windows_billboards),

    url(firstrun_re, views.FirstrunView.as_view(), name='firefox.firstrun'),
    url(whatsnew_re, views.WhatsnewView.as_view(), name='firefox.whatsnew'),
    url(whatsnew_re_b, views.WhatsnewViewGATest.as_view(), name='firefox.whatsnew.b'),
    url(tour_re, views.TourView.as_view(), name='firefox.tour'),

    # This dummy page definition makes it possible to link to /firefox/ (Bug 878068)
    url('^firefox/$', views.fx_home_redirect, name='firefox'),
    page('firefox/os', 'firefox/os/index.html'),
    page('firefox/os/releases', 'firefox/os/releases.html'),

    # firefox/os/notes/ should redirect to the latest version; update this in /redirects/urls.py
    url('^firefox/os/notes/(?P<fx_version>%s)/$' % version_re,
        views.release_notes, {'product': 'Firefox OS'},
        name='firefox.os.releasenotes'),

    page('mwc', 'firefox/os/mwc-2014-preview.html'),
    page('firefox/os/devices', 'firefox/os/devices.html'),

    url(releasenotes_re, views.release_notes, name='firefox.releasenotes'),
    url(mobile_releasenotes_re, views.release_notes,
        {'product': 'Firefox for Android'}, name='mobile.releasenotes'),
    url(sysreq_re, views.system_requirements,
        name='firefox.system_requirements'),
)
