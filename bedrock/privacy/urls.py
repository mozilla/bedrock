# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.mozorg.util import page
from bedrock.privacy import views

urlpatterns = (
    path("", views.privacy, name="privacy"),
    page("principles/", "privacy/principles.html", ftl_files=["privacy/principles", "privacy/index"]),
    page("faq/", "privacy/faq.html", ftl_files=["privacy/faq", "privacy/index"]),
    page("email/", "privacy/email.html", active_locales=["en-US", "de", "fr"]),
    path("betterweb/", views.firefox_betterweb_notices, name="privacy.notices.firefox-betterweb"),
    path("firefox/", views.firefox_notices, name="privacy.notices.firefox"),
    path("firefox-fire-tv/", views.firefox_fire_tv_notices, name="privacy.notices.firefox-fire-tv"),
    path("firefox-focus/", views.firefox_focus_notices, name="privacy.notices.firefox-focus"),
    path("firefox-reality/", views.firefox_reality_notices, name="privacy.notices.firefox-reality"),
    # bug 1319207 - special URL for Firefox Focus in de locale
    path("firefox-klar/", views.firefox_focus_notices, name="privacy.notices.firefox-klar"),
    path("hubs/", views.hubs_notices, name="privacy.notices.hubs"),
    path("thunderbird/", views.thunderbird_notices, name="privacy.notices.thunderbird"),
    path("websites/", views.websites_notices, name="privacy.notices.websites"),
    page("websites/data-preferences/", "privacy/data-preferences.html", ftl_files=["privacy/data-preferences"]),
    path("facebook/", views.facebook_notices, name="privacy.notices.facebook"),
    path("firefox-monitor/", views.firefox_monitor_notices, name="privacy.notices.firefox-monitor"),
    path("firefox-private-network/", views.firefox_private_network, name="privacy.notices.firefox-private-network"),
    path("firefox-relay/", views.firefox_relay_notices, name="privacy.notices.firefox-relay"),
    path("mozilla-vpn/", views.mozilla_vpn, name="privacy.notices.mozilla-vpn"),
    path("mdn-plus/", views.mdn_plus, name="privacy.notices.mdn-plus"),
    page("archive/", "privacy/archive/index.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2006-10/", "privacy/archive/firefox-2006-10.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2008-06/", "privacy/archive/firefox-2008-06.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2009-01/", "privacy/archive/firefox-2009-01.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2009-09/", "privacy/archive/firefox-2009-09.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2010-01/", "privacy/archive/firefox-2010-01.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2010-12/", "privacy/archive/firefox-2010-12.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2011-06/", "privacy/archive/firefox-2011-06.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2012-06/", "privacy/archive/firefox-2012-06.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2012-09/", "privacy/archive/firefox-2012-09.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2012-12/", "privacy/archive/firefox-2012-12.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox/2013-05/", "privacy/archive/firefox-2013-05.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox-cliqz/2018-06/", "privacy/archive/firefox-cliqz-2018-06.html", ftl_files=["privacy/index"], active_locales=["de", "en-US"]),
    page(
        "archive/firefox-marketplace/2015-01/",
        "privacy/archive/firefox-marketplace-2015-01.html",
        ftl_files=["privacy/index"],
        active_locales=["de", "en-US"],
    ),
    page("archive/firefox/third-party/", "privacy/archive/firefox-third-party.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/hello/2014-11/", "privacy/archive/hello-2014-11.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/hello/2016-03/", "privacy/archive/hello-2016-03.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/thunderbird/2010-06/", "privacy/archive/thunderbird-2010-06.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/websites/2013-08/", "privacy/archive/websites-2013-08.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/persona/2017-07/", "privacy/archive/persona-2017-07.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
    page("archive/firefox-os/2022-05/", "privacy/archive/firefox-os-2022-05.html", ftl_files=["privacy/index"], active_locales=["en-US"]),
)
