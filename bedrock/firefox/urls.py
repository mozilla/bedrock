# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

from bedrock.mozorg.util import page

import views
import bedrock.releasenotes.views
from bedrock.releasenotes import version_re
from bedrock.utils.views import VariationTemplateView


latest_re = r'^firefox(?:/(?P<version>%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')
tracking_protection_re = latest_re % (version_re, 'tracking-protection/start')
platform_re = '(?P<platform>android|ios)'
channel_re = '(?P<channel>beta|aurora|developer|nightly|organizations)'
releasenotes_re = latest_re % (version_re, r'(aurora|release)notes')
android_releasenotes_re = releasenotes_re.replace('firefox', 'firefox/android')
ios_releasenotes_re = releasenotes_re.replace('firefox', 'firefox/ios')
sysreq_re = latest_re % (version_re, 'system-requirements')
android_sysreq_re = sysreq_re.replace('firefox', 'firefox/android')
ios_sysreq_re = sysreq_re.replace('firefox', 'firefox/ios')


urlpatterns = (
    # Issue 5944 pre-download newsletter test.
    # When removing this experiment, please remember to unskip the
    # functional test in /test/functional/firefox/test_home.py
    url(r'^firefox/$',
        VariationTemplateView.as_view(template_name='firefox/home.html',
                                      template_context_variations=['a', 'b', 'c'],
                                      template_name_variations=['a', 'b', 'c'],
                                      variation_locales=['en-US']),
        name='firefox'),
    url(r'^firefox/(?:%s/)?(?:%s/)?all/$' % (platform_re, channel_re),
        views.all_downloads, name='firefox.all'),
    page('firefox/accounts', 'firefox/accounts.html'),
    url('^firefox/accounts/features/$',
        VariationTemplateView.as_view(
            template_name='firefox/accounts-features.html',
            template_context_variations=['a', 'b']),
            name='firefox.accounts-features'),
    page('firefox/channel/desktop', 'firefox/channel/desktop.html'),
    page('firefox/channel/android', 'firefox/channel/android.html'),
    page('firefox/channel/ios', 'firefox/channel/ios.html'),
    page('firefox/developer', 'firefox/developer/index.html'),
    page('firefox/election', 'firefox/election/index.html'),
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
    page('firefox/features/send-tabs', 'firefox/features/send-tabs.html'),
    page('firefox/features/sync', 'firefox/features/sync.html'),
    url(r'^firefox/ios/testflight/$', views.ios_testflight, name='firefox.ios.testflight'),
    page('firefox/mobile', 'firefox/mobile.html'),
    url('^firefox/send-to-device-post/$', views.send_to_device_ajax,
        name='firefox.send-to-device-post'),
    page('firefox/unsupported-systems', 'firefox/unsupported-systems.html'),
    url(r'^firefox/new/$', views.new, name='firefox.new'),
    url(r'^firefox/download/thanks/$', views.download_thanks, name='firefox.download.thanks'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    url(r'^firefox/installer-help/$', views.installer_help,
        name='firefox.installer-help'),
    url(firstrun_re, views.FirstrunView.as_view(), name='firefox.firstrun'),
    url(whatsnew_re, views.WhatsnewView.as_view(), name='firefox.whatsnew'),
    url(tracking_protection_re, views.TrackingProtectionTourView.as_view(),
        name='firefox.tracking-protection-tour.start'),

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

    # Bug 1108828. Different templates for different URL params.
    url('firefox/feedback/$', views.FeedbackView.as_view(), name='firefox.feedback'),

    url('^firefox/stub_attribution_code/$', views.stub_attribution_code,
        name='firefox.stub_attribution_code'),

    page('firefox/switch', 'firefox/switch.html'),
    page('firefox/pocket', 'firefox/pocket.html'),

    # Bug 1474285
    page('firefox/profile-migrate', 'firefox/profile/profile-migrate.html'),
    page('firefox/profile-downgrade', 'firefox/profile/profile-downgrade.html'),
)
