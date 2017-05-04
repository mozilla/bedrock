# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

from bedrock.redirects.util import redirect
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
    redirect(r'^firefox/$', 'firefox.new', name='firefox', locale_prefix=False),
    url(r'^firefox/(?:%s/)?(?:%s/)?all/$' % (platform_re, channel_re),
        views.all_downloads, name='firefox.all'),
    page('firefox/accounts', 'firefox/accounts.html'),
    page('firefox/channel/desktop', 'firefox/channel/desktop.html'),
    page('firefox/channel/android', 'firefox/channel/android.html'),
    page('firefox/channel/ios', 'firefox/channel/ios.html'),
    page('firefox/desktop', 'firefox/desktop/index.html'),
    page('firefox/desktop/fast', 'firefox/desktop/fast.html'),
    page('firefox/desktop/customize', 'firefox/desktop/customize.html'),
    page('firefox/desktop/tips', 'firefox/desktop/tips.html'),
    page('firefox/desktop/trust', 'firefox/desktop/trust.html'),
    page('firefox/developer', 'firefox/developer.html'),
    url(r'firefox/features/$', views.features_landing, name='firefox.features'),
    url('^firefox/features/private-browsing/$',
        views.FeaturesPrivateBrowsingView.as_view(),
        name='firefox.features.private-browsing'),
    url('^firefox/features/independent/$',
        views.FeaturesIndependentView.as_view(),
        name='firefox.features.independent'),
    url('^firefox/features/fast/$',
        views.FeaturesFastView.as_view(),
        name='firefox.features.fast'),
    page('firefox/geolocation', 'firefox/geolocation.html'),
    page('firefox/interest-dashboard', 'firefox/interest-dashboard.html'),
    page('firefox/android', 'firefox/android/index.html'),
    page('firefox/android/faq', 'firefox/android/faq.html'),
    page('firefox/ios', 'firefox/ios.html'),
    url(r'^firefox/ios/testflight', views.ios_testflight, name='firefox.ios.testflight'),
    page('firefox/mobile-download', 'firefox/mobile-download.html'),
    page('firefox/mobile-download/desktop', 'firefox/mobile-download-desktop.html'),
    url('^firefox/products/$',
        VariationTemplateView.as_view(template_name='firefox/family/index.html',
                                      template_name_variations=['b'],
                                      variation_locales=['en-US']),
        name='firefox.family.index'),
    page('firefox/private-browsing', 'firefox/private-browsing.html'),
    url('^firefox/send-to-device-post/$', views.send_to_device_ajax,
        name='firefox.send-to-device-post'),
    url(r'^firefox/sync/$',
        VariationTemplateView.as_view(template_name='firefox/sync.html',
                                      template_context_variations=['2', '3'],
                                      variation_locales=['en-US']),
        name='firefox.sync'),
    page('firefox/unsupported-systems', 'firefox/unsupported-systems.html'),
    url(r'^firefox/new/$', views.new, name='firefox.new'),
    page('firefox/organizations/faq', 'firefox/organizations/faq.html'),
    page('firefox/organizations', 'firefox/organizations/organizations.html'),
    page('firefox/nightly/firstrun', 'firefox/nightly_firstrun.html'),
    url(r'^firefox/installer-help/$', views.installer_help,
        name='firefox.installer-help'),

    page('firefox/unsupported/warning', 'firefox/unsupported/warning.html'),
    page('firefox/unsupported/EOL', 'firefox/unsupported/EOL.html'),
    page('firefox/unsupported/mac', 'firefox/unsupported/mac.html'),
    page('firefox/unsupported/details', 'firefox/unsupported/details.html'),

    # bug 960651
    # here because it needs to come after the above rule
    redirect(r'(firefox|mobile)/([^/]+)/details(/|/.+\.html)?$', 'firefox.unsupported.details',
             locale_prefix=False),

    url(r'^firefox/unsupported/win/$', views.windows_billboards),
    url('^firefox/dnt/$', views.dnt, name='firefox.dnt'),
    url(firstrun_re, views.FirstrunView.as_view(), name='firefox.firstrun'),
    url(whatsnew_re, views.WhatsnewView.as_view(), name='firefox.whatsnew'),

    url(tracking_protection_re, views.TrackingProtectionTourView.as_view(),
        name='firefox.tracking-protection-tour.start'),

    # This dummy page definition makes it possible to link to /firefox/ (Bug 878068)
    url('^firefox/$', views.fx_home_redirect, name='firefox'),

    # Release notes
    url('^firefox/(?:%s/)?(?:%s/)?notes/$' % (platform_re, channel_re),
        bedrock.releasenotes.views.latest_notes, name='firefox.notes'),
    url('firefox/(?:latest/)?releasenotes/$', bedrock.releasenotes.views.latest_notes,
        {'product': 'firefox'}),
    url('^firefox/(?:%s/)?system-requirements/$' % channel_re,
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
    url('firefox/feedback', views.FeedbackView.as_view(), name='firefox.feedback'),

    url('^firefox/stub_attribution_code/$', views.stub_attribution_code,
        name='firefox.stub_attribution_code'),
)
