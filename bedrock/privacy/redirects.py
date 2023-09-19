# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import no_redirect, redirect

redirectpatterns = (
    # bug 1319207
    # 'Firefox Focus' cannot be used in de locale due to legal constraints
    redirect(r"^de/privacy/firefox-focus/?", "/de/privacy/firefox-klar/", locale_prefix=False),
    # special de URL should not be accessible from other locales
    no_redirect(r"^de/privacy/firefox-klar/?", locale_prefix=False),
    redirect(r"^privacy/firefox-klar/?", "privacy.notices.firefox-focus"),
    # bug 1321033 - Hello EOL
    redirect(r"^privacy/firefox-hello/?$", "privacy.archive.hello-2016-03"),
    # bug 1394042 - Firefox Cloud Services redirect to Fx
    redirect(r"^privacy/firefox-cloud/?$", "privacy.notices.firefox"),
    # mozilla/bedrock/#5745 - archive cliqz policy
    redirect(r"^privacy/firefox-cliqz/?$", "privacy.archive.firefox-cliqz-2018-06"),
    # mozilla/bedrock/#7983
    redirect(r"^/privacy/products/?$", "firefox.privacy.products"),
    # mozilla/bedrock/#11610
    redirect(r"^privacy/firefox-os/?$", "privacy.archive.firefox-os-2022-05"),
    # issue 12156
    redirect(r"^privacy/(mozilla-vpn|firefox-relay)/?$", "privacy.notices.subscription-services"),
    # issue 12935
    redirect(r"^privacy/facebook/?$", "privacy.archive.facebook-2023-04"),
    # issue 13272
    redirect(r"^privacy/firefox-private-network/?$", "privacy.archive.firefox-private-network-notice-2023-06"),
    redirect(r"^privacy/betterweb/?$", "privacy.archive.firefox-betterweb-2023-06"),
    redirect(r"^privacy/firefox-fire-tv/?$", "privacy.archive.firefox-fire-tv-2023-06"),
    redirect(r"^privacy/firefox-reality/?$", "privacy.archive.firefox-reality-notice-2023-06"),
    # temporary
    # remove test in map_globalconf.py as well
    redirect(r"^privacy/mozilla-accounts/?$", "privacy.notices.firefox", permanent=False, anchor="firefox-accounts"),
)
