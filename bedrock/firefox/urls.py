# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

import bedrock.releasenotes.views
from bedrock.mozorg.util import page
from bedrock.releasenotes import version_re

from bedrock.firefox import views

latest_re = r'^firefox(?:/(?P<version>%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')
whatsnew_re_india = latest_re % (version_re, 'whatsnew/india')
whatsnew_re_all = latest_re % (version_re, 'whatsnew/all')
platform_re = '(?P<platform>android|ios)'
channel_re = '(?P<channel>beta|aurora|developer|nightly|organizations)'
releasenotes_re = latest_re % (version_re, r'(aurora|release)notes')
android_releasenotes_re = releasenotes_re.replace(r'firefox', 'firefox/android')
ios_releasenotes_re = releasenotes_re.replace(r'firefox', 'firefox/ios')
sysreq_re = latest_re % (version_re, 'system-requirements')
android_sysreq_re = sysreq_re.replace(r'firefox', 'firefox/android')
ios_sysreq_re = sysreq_re.replace(r'firefox', 'firefox/ios')


urlpatterns = (
    url(r'^firefox/$', views.firefox_home, name='firefox'),
    url(r'^firefox/all/$', views.firefox_all, name='firefox.all'),
    url(r'^firefox/accounts/$', views.firefox_accounts, name='firefox.accounts'),
    page('firefox/browsers', 'firefox/browsers/index.html'),
    page('firefox/products', 'firefox/products/index.html'),
    url(r'^firefox/campaign/$', views.campaign, name='firefox.campaign'),
    page('firefox/flashback', 'firefox/flashback/index.html', active_locales=['en-US', 'de', 'fr']),
    page('firefox/channel/desktop', 'firefox/channel/desktop.html'),
    page('firefox/channel/android', 'firefox/channel/android.html'),
    page('firefox/channel/ios', 'firefox/channel/ios.html'),
    page('firefox/developer', 'firefox/developer/index.html'),
    url('firefox/election/$', views.election_with_cards, name='firefox.election'),
    page('firefox/enterprise', 'firefox/enterprise/index.html'),
    page('firefox/enterprise/signup', 'firefox/enterprise/signup.html'),
    page('firefox/enterprise/signup/thanks', 'firefox/enterprise/signup-thanks.html'),
    page('firefox/facebookcontainer', 'firefox/facebookcontainer/index.html'),
    page('firefox/features', 'firefox/features/index.html'),
    url('^firefox/features/bookmarks/$',
        views.FeaturesBookmarksView.as_view(),
        name='firefox.features.bookmarks'),
    url('^firefox/features/fast/$',
        views.FeaturesFastView.as_view(),
        name='firefox.features.fast'),
    url('^firefox/features/independent/$',
        views.FeaturesIndependentView.as_view(),
        name='firefox.features.independent'),
    url('^firefox/features/memory/$',
        views.FeaturesMemoryView.as_view(),
        name='firefox.features.memory'),
    url('^firefox/features/password-manager/$',
        views.FeaturesPasswordManagerView.as_view(),
        name='firefox.features.password-manager'),
    url('^firefox/features/private-browsing/$',
        views.FeaturesPrivateBrowsingView.as_view(),
        name='firefox.features.private-browsing'),
    url(r'^firefox/ios/testflight/$', views.ios_testflight, name='firefox.ios.testflight'),
    page('firefox/mobile', 'firefox/mobile/index.html'),
    page('firefox/mobile/get-app', 'firefox/mobile/get-app.html'),
    url('^firefox/send-to-device-post/$', views.send_to_device_ajax,
        name='firefox.send-to-device-post'),
    page('firefox/unsupported-systems', 'firefox/unsupported-systems.html'),
    url(r'^firefox/new/$', views.new, name='firefox.new'),
    url(r'^firefox/download/thanks/$', views.download_thanks, name='firefox.download.thanks'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    url(r'^firefox/installer-help/$', views.installer_help,
        name='firefox.installer-help'),
    url(firstrun_re, views.FirstrunView.as_view(), name='firefox.firstrun'),
    url(whatsnew_re, views.WhatsNewRedirectorView.as_view(), name='firefox.whatsnew'),
    url(whatsnew_re_india, views.WhatsNewIndiaView.as_view(), name='firefox.whatsnew.india'),
    url(whatsnew_re_all, views.WhatsnewView.as_view(), name='firefox.whatsnew.all'),

    page('firefox/features/adblocker', 'firefox/features/adblocker.html'),

    # Release notes
    url('^firefox/(?:%s/)?(?:%s/)?notes/$' % (platform_re, channel_re),
        bedrock.releasenotes.views.latest_notes, name='firefox.notes'),
    url('^firefox/nightly/notes/feed/$',
        bedrock.releasenotes.views.nightly_feed, name='firefox.nightly.notes.feed'),
    url('firefox/(?:latest/)?releasenotes/$', bedrock.releasenotes.views.latest_notes,
        {'product': 'firefox'}),
    url('^firefox/(?:%s/)?(?:%s/)?system-requirements/$' % (platform_re, channel_re),
        bedrock.releasenotes.views.latest_sysreq,
        {'product': 'firefox'}, name='firefox.sysreq'),
    url(releasenotes_re, bedrock.releasenotes.views.release_notes, name='firefox.desktop.releasenotes'),
    url(android_releasenotes_re, bedrock.releasenotes.views.release_notes,
        {'product': 'Firefox for Android'}, name='firefox.android.releasenotes'),
    url(ios_releasenotes_re, bedrock.releasenotes.views.release_notes,
        {'product': 'Firefox for iOS'}, name='firefox.ios.releasenotes'),
    url(sysreq_re, bedrock.releasenotes.views.system_requirements,
        name='firefox.system_requirements'),
    url(android_sysreq_re, bedrock.releasenotes.views.system_requirements,
        {'product': 'Firefox for Android'}, name='firefox.android.system_requirements'),
    url(ios_sysreq_re, bedrock.releasenotes.views.system_requirements,
        {'product': 'Firefox for iOS'}, name='firefox.ios.system_requirements'),
    url('^firefox/releases/$', bedrock.releasenotes.views.releases_index,
        {'product': 'Firefox'}, name='firefox.releases.index'),

    url('^firefox/stub_attribution_code/$', views.stub_attribution_code,
        name='firefox.stub_attribution_code'),

    url(r'^firefox/welcome/1/$', views.firefox_welcome_page1, name='firefox.welcome.page1'),
    page('firefox/welcome/2', 'firefox/welcome/page2.html'),
    page('firefox/welcome/3', 'firefox/welcome/page3.html'),
    page('firefox/welcome/4', 'firefox/welcome/page4.html'),
    page('firefox/welcome/5', 'firefox/welcome/page5.html'),

    page('firefox/switch', 'firefox/switch.html'),
    page('firefox/pocket', 'firefox/pocket.html'),

    # Bug 1519084
    page('firefox/dedicated-profiles', 'firefox/dedicated-profiles.html'),

    # Issue 6178
    page('firefox/this-browser-comes-highly-recommended', 'firefox/recommended.html'),

    # Issue 6604, SEO firefox/new pages
    page('firefox/windows', 'firefox/new/scene1_windows.html'),
    page('firefox/mac', 'firefox/new/scene1_mac.html'),
    page('firefox/linux', 'firefox/new/scene1_linux.html'),

    page('firefox/windows-64-bit', 'firefox/windows-64-bit.html'),

    page('firefox/features/safebrowser', 'firefox/features/safebrowser.html'),
    page('firefox/best-browser', 'firefox/best-browser.html'),

    page('firefox/browsers/compare', 'firefox/compare/index.html'),
    page('firefox/browsers/compare/chrome', 'firefox/compare/chrome.html'),
    page('firefox/browsers/compare/ie', 'firefox/compare/ie.html'),
    page('firefox/browsers/compare/opera', 'firefox/compare/opera.html'),
    page('firefox/browsers/compare/safari', 'firefox/compare/safari.html'),
    page('firefox/browsers/compare/edge', 'firefox/compare/edge.html'),

    # Lockwise
    page('firefox/lockwise', 'firefox/lockwise/lockwise.html'),

    # Issue 7765, 7709
    page('firefox/privacy', 'firefox/privacy/index.html'),
    page('firefox/privacy/products', 'firefox/privacy/products.html'),

    # Issue 8432
    page('firefox/set-as-default/thanks', 'firefox/set-as-default/thanks.html'),
    # Default browser campaign
    page('firefox/set-as-default', 'firefox/set-as-default/landing-page.html')
)
