# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from bedrock.mozorg.util import page
from bedrock.privacy import views

urlpatterns = (
    url(r'^/$', views.privacy, name='privacy'),
    page('/principles', 'privacy/principles.html'),
    page('/faq', 'privacy/faq.html'),
    url(r'^/firefox/$', views.firefox_notices, name='privacy.notices.firefox'),
    url(r'^/firefox-os/$', views.firefox_os_notices, name='privacy.notices.firefox-os'),
    url(r'^/firefox-cliqz/$', views.firefox_cliqz_notices, name='privacy.notices.firefox-cliqz'),
    url(r'^/firefox-focus/$', views.firefox_focus_notices, name='privacy.notices.firefox-focus'),
    url(r'^/firefox-rocket/$', views.firefox_rocket_notices, name='privacy.notices.firefox-rocket'),
    # bug 1319207 - special URL for Firefox Focus in de locale
    url(r'^/firefox-klar/$', views.firefox_focus_notices, name='privacy.notices.firefox-klar'),
    url(r'^/thunderbird/$', views.thunderbird_notices, name='privacy.notices.thunderbird'),
    url(r'^/websites/$', views.websites_notices, name='privacy.notices.websites'),
    url(r'^/facebook/$', views.facebook_notices, name='privacy.notices.facebook'),

    page('/archive', 'privacy/archive/index.html'),
    page('/archive/firefox/2006-10', 'privacy/archive/firefox-2006-10.html'),
    page('/archive/firefox/2008-06', 'privacy/archive/firefox-2008-06.html'),
    page('/archive/firefox/2009-01', 'privacy/archive/firefox-2009-01.html'),
    page('/archive/firefox/2009-09', 'privacy/archive/firefox-2009-09.html'),
    page('/archive/firefox/2010-01', 'privacy/archive/firefox-2010-01.html'),
    page('/archive/firefox/2010-12', 'privacy/archive/firefox-2010-12.html'),
    page('/archive/firefox/2011-06', 'privacy/archive/firefox-2011-06.html'),
    page('/archive/firefox/2012-06', 'privacy/archive/firefox-2012-06.html'),
    page('/archive/firefox/2012-09', 'privacy/archive/firefox-2012-09.html'),
    page('/archive/firefox/2012-12', 'privacy/archive/firefox-2012-12.html'),
    page('/archive/firefox/2013-05', 'privacy/archive/firefox-2013-05.html'),
    page('/archive/firefox/third-party', 'privacy/archive/firefox-third-party.html'),
    page('/archive/hello/2014-11', 'privacy/archive/hello-2014-11.html'),
    page('/archive/hello/2016-03', 'privacy/archive/hello-2016-03.html'),
    page('/archive/thunderbird/2010-06', 'privacy/archive/thunderbird-2010-06.html'),
    page('/archive/websites/2013-08', 'privacy/archive/websites-2013-08.html'),
    page('/archive/persona/2017-07', 'privacy/archive/persona-2017-07.html'),
)
