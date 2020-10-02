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
    page('firefox', 'exp/firefox/index.html', ftl_files=['firefox/home']),
    url(r'^firefox/new/$', views.new, name='exp.firefox.new'),
    page('firefox/mobile', 'exp/firefox/mobile.html', ftl_files=['firefox/mobile']),
    url(r'^$', views.home_view, name='exp.mozorg.home'),
    page('firefox/accounts', 'exp/firefox/accounts.html', ftl_files=['firefox/accounts']),
    page('firefox/unfck', 'exp/firefox/campaign/unfck/index.html'),
)
