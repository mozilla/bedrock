# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import patterns, url

from commonware.response.decorators import xframe_allow

from bedrock.firefox import version_re
from bedrock.redirects.util import redirect
from bedrock.mozorg.util import page
import views


latest_re = r'^firefox(?:/(?P<fx_version>%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')
tour_re = latest_re % (version_re, 'tour')
product_re = '(?P<product>firefox|mobile)'
channel_re = '(?P<channel>beta|aurora|organizations)'
releasenotes_re = latest_re % (version_re, r'(aurora|release)notes')
mobile_releasenotes_re = releasenotes_re.replace('firefox', 'mobile')
sysreq_re = latest_re % (version_re, 'system-requirements')


urlpatterns = patterns('',
    redirect(r'^firefox/$', 'firefox.new', name='firefox'),
    url(r'^firefox/(?:%s/)?all/$' % channel_re,
        views.all_downloads, name='firefox.all'),
    page('firefox/channel', 'firefox/channel.html'),
    redirect('^firefox/channel/android/$', 'firefox.channel'),
    page('firefox/desktop', 'firefox/desktop/index.html'),
    page('firefox/desktop/fast', 'firefox/desktop/fast.html'),
    page('firefox/desktop/customize', 'firefox/desktop/customize.html'),
    page('firefox/desktop/tips', 'firefox/desktop/tips.html'),
    page('firefox/desktop/trust', 'firefox/desktop/trust.html'),
    page('firefox/geolocation', 'firefox/geolocation.html'),
    page('firefox/interest-dashboard', 'firefox/interest-dashboard.html'),
    url('^(?:%s)/(?:%s/)?notes/$' % (product_re, channel_re),
        views.latest_notes, name='firefox.notes'),
    url('^firefox/latest/releasenotes/$', views.latest_notes),
    url('^firefox/(?:%s/)?system-requirements/$' % channel_re,
        views.latest_sysreq, name='firefox.sysreq'),
    page('firefox/android', 'firefox/android/index.html'),
    page('firefox/android/faq', 'firefox/android/faq.html'),
    page('firefox/os/faq', 'firefox/os/faq.html'),
    url('^firefox/sms/$', views.sms_send, name='firefox.sms'),
    page('firefox/sms/sent', 'firefox/android/sms-thankyou.html'),
    page('firefox/sync', 'firefox/sync.html'),
    page('firefox/unsupported-systems', 'firefox/unsupported-systems.html'),
    page('firefox/new', 'firefox/new.html', decorators=xframe_allow),
    page('firefox/organizations/faq', 'firefox/organizations/faq.html'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    url('^firefox/releases/$', views.releases_index,
        name='firefox.releases.index'),
    url(r'^firefox/installer-help/$', views.installer_help,
        name='firefox.installer-help'),

    page('firefox/unsupported/warning', 'firefox/unsupported/warning.html'),
    page('firefox/unsupported/EOL', 'firefox/unsupported/EOL.html'),
    page('firefox/unsupported/mac', 'firefox/unsupported/mac.html'),
    page('firefox/unsupported/details', 'firefox/unsupported/details.html'),

    url(r'^firefox/unsupported/win/$', views.windows_billboards),
    url('^dnt/$', views.dnt, name='firefox.dnt'),
    url(firstrun_re, views.FirstrunView.as_view(), name='firefox.firstrun'),
    url(whatsnew_re, views.WhatsnewView.as_view(), name='firefox.whatsnew'),
    url(tour_re, views.TourView.as_view(), name='firefox.tour'),
    url(r'^firefox/partners/$', views.firefox_partners,
        name='firefox.partners.index'),

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
