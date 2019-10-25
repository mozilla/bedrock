# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from bedrock.mozorg.util import page
from bedrock.releasenotes import version_re
from bedrock.exp import views


latest_re = r'^firefox(?:/(?P<version>%s))?/%s/$'
whatsnew_re_all = latest_re % (version_re, 'whatsnew/all')

urlpatterns = (
    page('opt-out', 'exp/opt-out.html'),
    page('firefox', 'exp/firefox/index.html', active_locales=['en-US', 'en-GB', 'en-CA', 'de']),
    page('firefox/new', 'exp/firefox/new/download.html', active_locales=['en-US', 'en-GB', 'en-CA', 'de']),
    page('firefox/accounts', 'exp/firefox/accounts-2019.html'),
    page('firefox/lockwise', 'exp/firefox/lockwise.html', active_locales=['en-US', 'en-GB', 'en-CA', 'de']),
    page('firefox', 'exp/firefox/index.html', active_locales=['en-US', 'en-GB', 'en-CA', 'de']),
    page('firefox/welcome/1', 'exp/firefox/welcome/page1.html'),
    url(whatsnew_re_all, views.WhatsnewView.as_view(), name='exp.firefox.whatsnew.all'),
)
