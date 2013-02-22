# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from django.conf.urls.defaults import *
from django.conf import settings

from jingo_minify.helpers import BUILD_ID_JS, BUNDLE_HASHES
from product_details import product_details

from firefox import version_re
from redirects.util import redirect
from mozorg.util import page
import views


latest_re = r'^firefox(?:/(%s))?/%s/$'
firstrun_re = latest_re % (version_re, 'firstrun')
whatsnew_re = latest_re % (version_re, 'whatsnew')


def get_js_bundle_files(bundle):
    """
    Return a JSON string of the list of file names for lazy loaded
    javascript.
    """
    # mostly stolen from jingo_minify.helpers.js
    if settings.DEBUG:
        items = settings.MINIFY_BUNDLES['js'][bundle]
    else:
        build_id = BUILD_ID_JS
        bundle_full = "js:%s" % bundle
        if bundle_full in BUNDLE_HASHES:
            build_id = BUNDLE_HASHES[bundle_full]
        items = ("js/%s-min.js?build=%s" % (bundle, build_id,),)
    return json.dumps([settings.MEDIA_URL + i for i in items])


urlpatterns = patterns('',
    url(r'^firefox/all/$', views.all_downloads, name='firefox.all'),
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
    page('firefox/unsupported/mac', 'firefox/unsupported-mac.html'),

    url(r'^firefox/unsupported/win/$', views.windows_billboards),
    url('^dnt/$', views.dnt, name='firefox.dnt'),
    url(firstrun_re, views.latest_fx_redirect, name='firefox.firstrun',
        kwargs={'template_name': 'firefox/firstrun.html'}),
    url(whatsnew_re, views.latest_fx_redirect, name='firefox.whatsnew',
        kwargs={'template_name': 'firefox/whatsnew.html'}),

    page('firefox/partners', 'firefox/partners/index.html',
         js_common=get_js_bundle_files('partners_common'),
         js_mobile=get_js_bundle_files('partners_mobile'),
         js_desktop=get_js_bundle_files('partners_desktop')),
    url(r'^firefox/partners/contact-bizdev/', views.contact_bizdev,
        name='firefox.partners.contact-bizdev'),
)
