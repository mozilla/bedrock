# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

import bedrock.releasenotes.views
from bedrock.mozorg.util import page
from bedrock.releasenotes import version_re

from bedrock.firefox import views
from bedrock.utils import views as utils_views


latest_re = r'^firefox(?:/(?P<version>%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')
whatsnew_re_africa = latest_re % (version_re, 'whatsnew/africa')
whatsnew_re_india = latest_re % (version_re, 'whatsnew/india')
whatsnew_re_china = latest_re % (version_re, 'whatsnew/china')
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
    url(r'^firefox/$', views.FirefoxHomeView.as_view(), name='firefox'),
    url(r'^firefox/all/$', views.firefox_all, name='firefox.all'),
    page('firefox/accounts', 'firefox/accounts.html', ftl_files=['firefox/accounts']),
    page('firefox/browsers', 'firefox/browsers/index.html', ftl_files=['firefox/browsers']),
    page('firefox/products', 'firefox/products/index.html', ftl_files=['firefox/products']),
    page('firefox/flashback', 'firefox/flashback/index.html', active_locales=['en-US', 'de', 'fr']),
    page('firefox/channel/desktop', 'firefox/channel/desktop.html', ftl_files=['firefox/channel']),
    page('firefox/channel/android', 'firefox/channel/android.html', ftl_files=['firefox/channel']),
    page('firefox/channel/ios', 'firefox/channel/ios.html', ftl_files=['firefox/channel']),
    page('firefox/developer', 'firefox/developer/index.html'),
    page('firefox/enterprise', 'firefox/enterprise/index.html', ftl_files=['firefox/enterprise']),
    page('firefox/enterprise/signup', 'firefox/enterprise/signup.html'),
    page('firefox/enterprise/signup/thanks', 'firefox/enterprise/signup-thanks.html'),
    page('firefox/facebookcontainer', 'firefox/facebookcontainer/index.html', ftl_files=['firefox/facebook_container']),

    page('firefox/features', 'firefox/features/index.html',
         ftl_files=['firefox/features/shared', 'firefox/features/index']),
    page('firefox/features/adblocker', 'firefox/features/adblocker.html',
         ftl_files=['firefox/features/adblocker']),
    page('firefox/features/bookmarks', 'firefox/features/bookmarks.html',
         ftl_files=['firefox/features/shared', 'firefox/features/bookmarks']),
    page('firefox/features/fast', 'firefox/features/fast.html',
         ftl_files=['firefox/features/shared', 'firefox/features/fast']),
    page('firefox/features/independent', 'firefox/features/independent.html',
         ftl_files=['firefox/features/shared', 'firefox/features/independent']),
    page('firefox/features/memory', 'firefox/features/memory.html',
         ftl_files=['firefox/features/shared', 'firefox/features/memory']),
    page('firefox/features/password-manager', 'firefox/features/password-manager.html',
         ftl_files=['firefox/features/shared', 'firefox/features/password-manager']),
    page('firefox/features/private-browsing', 'firefox/features/private-browsing.html',
         ftl_files=['firefox/features/shared', 'firefox/features/private-browsing']),
    page('firefox/features/safebrowser', 'firefox/features/safebrowser.html'),

    url(r'^firefox/ios/testflight/$', views.ios_testflight, name='firefox.ios.testflight'),
    page('firefox/mobile', 'firefox/mobile/index.html', ftl_files=['firefox/mobile']),
    page('firefox/mobile/get-app', 'firefox/mobile/get-app.html', ftl_files=['firefox/mobile']),
    url('^firefox/send-to-device-post/$', views.send_to_device_ajax,
        name='firefox.send-to-device-post'),
    page('firefox/unsupported-systems', 'firefox/unsupported-systems.html'),
    url(r'^firefox/new/$', views.NewView.as_view(), name='firefox.new'),
    url(r'^firefox/download/thanks/$', views.DownloadThanksView.as_view(), name='firefox.download.thanks'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    url(r'^firefox/installer-help/$', views.InstallerHelpView.as_view(), name='firefox.installer-help'),
    url(firstrun_re, views.FirstrunView.as_view(), name='firefox.firstrun'),
    url(whatsnew_re, views.WhatsNewRedirectorView.as_view(), name='firefox.whatsnew'),
    url(whatsnew_re_africa, views.WhatsNewFirefoxLiteView.as_view(), name='firefox.whatsnew.africa'),
    url(whatsnew_re_india, views.WhatsNewFirefoxLiteView.as_view(), name='firefox.whatsnew.india'),
    url(whatsnew_re_china, views.WhatsNewChinaView.as_view(), name='firefox.whatsnew.china'),
    url(whatsnew_re_all, views.WhatsnewView.as_view(), name='firefox.whatsnew.all'),

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
    page('firefox/welcome/2', 'firefox/welcome/page2.html', ftl_files=['firefox/welcome/page2']),
    page('firefox/welcome/3', 'firefox/welcome/page3.html', ftl_files=['firefox/welcome/page3']),
    page('firefox/welcome/4', 'firefox/welcome/page4.html', ftl_files=['firefox/welcome/page4']),
    page('firefox/welcome/5', 'firefox/welcome/page5.html', ftl_files=['firefox/welcome/page5']),
    page('firefox/welcome/6', 'firefox/welcome/page6.html', ftl_files=['firefox/welcome/page6']),
    page('firefox/welcome/7', 'firefox/welcome/page7.html', ftl_files=['firefox/welcome/page7']),
    url(r'^firefox/welcome/8/$',
        utils_views.VariationTemplateView.as_view(
          template_name='firefox/welcome/page8.html',
          ftl_files=['firefox/welcome/page8'],
          template_context_variations=['text', 'image', 'animation', 'header-text'],
          variation_locales=['en-US', 'en-CA', 'en-GB', 'de', 'fr']),
        name='firefox.welcome.page8'),

    page('firefox/privacy-by-default', 'firefox/messaging-experiment/privacy_by_default.html'),
    page('firefox/privacy-tools', 'firefox/messaging-experiment/privacy_tools.html'),
    page('firefox/mobile-promo', 'firefox/messaging-experiment/control.html'),

    page('firefox/switch', 'firefox/switch.html', ftl_files=['firefox/switch']),
    page('firefox/pocket', 'firefox/pocket.html'),

    # Issue 6604, SEO firefox/new pages
    page('firefox/windows', 'firefox/new/protocol/download_windows.html'),
    page('firefox/mac', 'firefox/new/protocol/download_mac.html'),
    page('firefox/linux', 'firefox/new/protocol/download_linux.html'),

    page('firefox/browsers/compare', 'firefox/browsers/compare/index.html',
         ftl_files=['firefox/browsers/compare/index', 'firefox/browsers/compare/shared']),
    page('firefox/browsers/compare/brave', 'firefox/browsers/compare/brave.html',
         ftl_files=['firefox/browsers/compare/brave', 'firefox/browsers/compare/shared']),
    page('firefox/browsers/compare/chrome', 'firefox/browsers/compare/chrome.html',
         ftl_files=['firefox/browsers/compare/chrome', 'firefox/browsers/compare/shared']),
    page('firefox/browsers/compare/edge', 'firefox/browsers/compare/edge.html',
         ftl_files=['firefox/browsers/compare/edge', 'firefox/browsers/compare/shared']),
    page('firefox/browsers/compare/ie', 'firefox/browsers/compare/ie.html',
         ftl_files=['firefox/browsers/compare/ie', 'firefox/browsers/compare/shared']),
    page('firefox/browsers/compare/opera', 'firefox/browsers/compare/opera.html',
         ftl_files=['firefox/browsers/compare/opera', 'firefox/browsers/compare/shared']),
    page('firefox/browsers/compare/safari', 'firefox/browsers/compare/safari.html',
         ftl_files=['firefox/browsers/compare/safari', 'firefox/browsers/compare/shared']),

    # Issue 8641
    page('firefox/browsers/best-browser', 'firefox/browsers/best-browser.html'),
    page('firefox/browsers/browser-history', 'firefox/browsers/browser-history.html'),
    page('firefox/browsers/incognito-browser', 'firefox/browsers/incognito-browser.html'),
    page('firefox/browsers/update-your-browser', 'firefox/browsers/update-browser.html'),
    page('firefox/browsers/what-is-a-browser', 'firefox/browsers/what-is-a-browser.html'),
    page('firefox/browsers/windows-64-bit', 'firefox/browsers/windows-64-bit.html'),

    # Lockwise
    page('firefox/lockwise', 'firefox/products/lockwise.html', ftl_files=['firefox/products/lockwise']),

    # Issue 7765, 7709
    page('firefox/privacy', 'firefox/privacy/index.html', ftl_files=['firefox/privacy-hub']),
    page('firefox/privacy/products', 'firefox/privacy/products.html', ftl_files=['firefox/privacy-hub']),

    # Issue 8432
    page('firefox/set-as-default/thanks', 'firefox/set-as-default/thanks.html', ftl_files='firefox/set-as-default/thanks'),
    # Default browser campaign
    page('firefox/set-as-default', 'firefox/set-as-default/landing.html', ftl_files='firefox/set-as-default/landing'),

    # Issue 8536
    page('firefox/retention/thank-you', 'firefox/retention/thank-you.html'),

    # Unfck campaign
    page('firefox/unfck', 'firefox/campaign/unfck/index.html', active_locales=['de', 'en-US', 'fr']),

    # Issue #9490 - Evergreen Content for SEO
    page('firefox/more', 'firefox/more.html', ftl_files='firefox/more'),
    page('firefox/browsers/quantum', 'firefox/browsers/quantum.html', ftl_files='firefox/browsers/quantum'),
    page('firefox/faq', 'firefox/faq.html', ftl_files='firefox/faq'),
    page('firefox/browsers/chromebook', 'firefox/browsers/chromebook.html', ftl_files='firefox/browsers/chromebook'),
    page('firefox/sync', 'firefox/sync.html', ftl_files='firefox/sync'),
)
