# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

from .base import flatten, url_test

UA_ANDROID = {"User-Agent": "Mozilla/5.0 (Android 6.0.1; Mobile; rv:51.0) Gecko/51.0 Firefox/51.0"}
UA_IOS = {"User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8F190"}

FXC_WITH_DEFAULT_QS = "https://www.firefox.com/?redirect_source=mozilla-org"
FIREFOX_UPDATE_URL = (
    "https://www.firefox.com/?redirect_source=mozilla-org&utm_source=firefox-browser&utm_medium=firefox-browser&utm_campaign=firefox-update-redirect"
)

QUERY_STRING = {"redirect_source": "mozilla-org"}

if settings.ENABLE_PERMANENT_FIREFOX_COM_REDIRECTS:
    STATUS_CODE = 301
else:
    STATUS_CODE = 302

URLS = flatten(
    (
        url_test("/firefox/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # firefox/beta/all
        url_test(
            "/firefox/beta/all/",
            "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org#beta",
            status_code=STATUS_CODE,
        ),
        # firefox/developer/all
        url_test(
            "/firefox/developer/all/",
            "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org#developer",
            status_code=STATUS_CODE,
        ),
        # firefox/aurora/all
        url_test(
            "/firefox/aurora/all/",
            "https://www.firefox.com/channel/desktop/developer/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # firefox/nightly/all
        url_test(
            "/firefox/nightly/all/",
            "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org#nightly",
            status_code=STATUS_CODE,
        ),
        # firefox/organizations/all
        url_test(
            "/firefox/organizations/all/",
            "https://www.firefox.com/browsers/enterprise/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # firefox/android/all
        url_test(
            "/firefox/android/all/",
            "https://www.firefox.com/browsers/mobile/android/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # firefox/android/beta/all
        url_test(
            "/firefox/android/beta/all/",
            "https://www.firefox.com/download/all/android-beta/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # firefox/android/nightly/all
        url_test(
            "/firefox/android/nightly/all/",
            "https://www.firefox.com/download/all/android-nightly/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # mobile beta/aurora/nightly
        url_test(
            "/mobile/beta/",
            "https://www.firefox.com/channel/android/?redirect_source=mozilla-org#beta",
            status_code=STATUS_CODE,
        ),
        url_test(
            "/mobile/aurora/",
            "https://www.firefox.com/channel/android/?redirect_source=mozilla-org#aurora",
            status_code=STATUS_CODE,
        ),
        url_test(
            "/mobile/nightly/",
            "https://www.firefox.com/channel/android/?redirect_source=mozilla-org#nightly",
            status_code=STATUS_CODE,
        ),
        # firefox/unsupported-systems.html
        url_test(
            "/firefox/unsupported-systems.html",
            "https://www.firefox.com/browsers/unsupported-systems/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # mobile/notes
        url_test("/mobile/notes/", "https://www.firefox.com/firefox/android/notes/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/mobile/beta/notes/", "https://www.firefox.com/firefox/android/beta/notes/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test(
            "/mobile/aurora/notes/", "https://www.firefox.com/firefox/android/aurora/notes/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        # system requirements
        url_test(
            "/firefox/system-requirements",
            "https://www.firefox.com/firefox/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        url_test(
            "/firefox/system-requirements.html",
            "https://www.firefox.com/firefox/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        url_test(
            "/firefox/beta/system-requirements",
            "https://www.firefox.com/firefox/beta/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        url_test(
            "/firefox/aurora/system-requirements",
            "https://www.firefox.com/firefox/aurora/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        url_test(
            "/firefox/organizations/system-requirements",
            "https://www.firefox.com/firefox/organizations/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # download URLs
        url_test("/download/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/download", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/mobile/download", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # all downloads
        url_test("/firefox/all", "https://www.firefox.com/download/all/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/all.html", "https://www.firefox.com/download/all/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # search
        url_test("/firefox/search", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/search.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # beta/aurora downloads
        url_test("/firefox/all-beta", "https://www.firefox.com/download/all/desktop-beta/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/all-beta.html", "https://www.firefox.com/download/all/desktop-beta/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/all-rc", "https://www.firefox.com/download/all/desktop-beta/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/all-rc.html", "https://www.firefox.com/download/all/desktop-beta/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test(
            "/firefox/all-aurora", "https://www.firefox.com/download/all/desktop-developer/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test(
            "/firefox/all-aurora.html", "https://www.firefox.com/download/all/desktop-developer/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test("/firefox/aurora/all/", "https://www.firefox.com/channel/desktop/developer/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # aurora pages
        url_test("/firefox/aurora/notes/", "https://www.firefox.com/firefox/developer/notes/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test(
            "/firefox/aurora/system-requirements/",
            "https://www.firefox.com/firefox/developer/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # ESR downloads
        url_test(
            "/firefox/organizations/all.html",
            "https://www.firefox.com/download/all/desktop-esr/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # mobile sync
        url_test("/mobile/sync", "https://www.firefox.com/features/sync/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # toolkit download to devices
        url_test("/firefox/toolkit/download-to-your-devices", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # firefox update
        url_test("/firefox/update", FIREFOX_UPDATE_URL, status_code=STATUS_CODE),
        # mobile features
        url_test("/mobile/features/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/mobile/features/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/m/features/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # m/ redirect
        url_test("/m/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # all-older.html
        url_test("/firefox/all-older.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # central/sync pages
        url_test("/firefox/start/central.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/products/firefox/start/central.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/sync/firstrun.html", "https://www.firefox.com/features/sync/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # fx redirects
        url_test("/firefox/fx", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/fx/whatever", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # performance pages
        url_test("/firefox/performance/", "https://www.firefox.com/features/fast/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/happy/", "https://www.firefox.com/features/fast/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/speed/", "https://www.firefox.com/features/fast/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/memory/", "https://www.firefox.com/features/fast/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/security/", "https://www.firefox.com/features/private/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # central pages
        url_test("/firefox/central/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/central.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/central-lite.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/products/firefox/central/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # SMS redirects
        url_test("/firefox/sms/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/sms/whatever/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Code name redirects
        url_test("/projects/bonecho/", "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/projects/deerpark/", "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/projects/granparadiso/", "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/projects/minefield/", "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/projects/namoroka/", "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/projects/shiretoko/", "https://www.firefox.com/channel/desktop/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Firebird
        url_test("/products/firebird/compare/", "https://www.firefox.com?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/products/firebird/", "https://www.firefox.com?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/products/firebird/download/", "https://www.firefox.com?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Fennic
        url_test("/fennec/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Mobile
        url_test("/mobile/", "https://www.firefox.com/browser/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/mobile/customize/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/mobile/customize/whatever/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Firefox independent/personal
        url_test("/firefox/independent/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/personal/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Firefox upgrade/IE
        url_test("/firefox/upgrade", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/ie", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Sync
        url_test("/sync/", "https://www.firefox.com/features/sync/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # FxAndroid
        url_test("/fxandroid/", "https://www.firefox.com/browsers/mobile/android/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Upper-case Firefox
        url_test("/Firefox/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # firefox/desktop pages
        url_test("/firefox/desktop/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/desktop/fast/", "https://www.firefox.com/features/fast/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/desktop/trust/", "https://www.firefox.com/features/private/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/desktop/tips/", "https://www.firefox.com/features/tips/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Firefox Android/Focus/iOS
        url_test("/firefox/android/", "https://www.firefox.com/browsers/mobile/android/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/focus/", "https://www.firefox.com/browsers/mobile/focus/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test(
            "/firefox/browsers/mobile/compare/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test("/firefox/ios/", "https://www.firefox.com/browsers/mobile/ios/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Organizations
        url_test("/firefox/organizations/faq/", "https://www.firefox.com/enterprise/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/organizations/", "https://www.firefox.com/enterprise/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Mobile download
        url_test("/firefox/mobile-download/", "https://www.firefox.com/browsers/mobile/index/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test(
            "/firefox/mobile-download/whatever/",
            "https://www.firefox.com/browsers/mobile/index/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # details redirects
        url_test(
            "/firefox/56.0/details/", "https://www.firefox.com/browsers/unsupported-systems/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test(
            "/mobile/56.0/details/", "https://www.firefox.com/browsers/unsupported-systems/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test(
            "/firefox/unsupported/", "https://www.firefox.com/browsers/unsupported-systems/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        # Various redirects
        url_test("/firefox/tips", "https://www.firefox.com/features/tips/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/new/something", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test(
            "/firefox/38.0.3/releasenotes/",
            "https://www.firefox.com/firefox/38.0.5/releasenotes/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        url_test("/firefox/default.htm", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test(
            "/firefox/android/56.0", "https://www.firefox.com/firefox/android/56.0/releasenotes/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test("/firefox/stats/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # vote and election
        url_test("/vote/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/election/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Firefox HTML
        url_test("/firefox/firefox.html", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Misc promotional pages
        url_test("/firefoxfightsforyou/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/fights-for-you/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/flashback/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/browsers/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/firefox/campaign/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Enterprise
        url_test("/firefox/enterprise/signup/", "https://www.firefox.com/enterprise/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Features
        url_test(
            "/firefox/features/pip/", "https://www.firefox.com/features/picture-in-picture/?redirect_source=mozilla-org", status_code=STATUS_CODE
        ),
        url_test("/firefox/features/memory/", "https://www.firefox.com/features/fast/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/features/independent/", "https://www.firefox.com/features/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/features/safebrowser/", "https://www.firefox.com/features/private/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/sync/", "https://www.firefox.com/features/sync/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/mobile/get-app/", "https://www.firefox.com/browsers/mobile/get-app/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test(
            "/firefox/privacy/safe-passwords/",
            "https://www.firefox.com/features/password-manager/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        # Windows/browser specific
        url_test("/firefox/windows-64-bit/", "https://www.firefox.com/more/windows-64-bit/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/firefox/best-browser/", "https://www.firefox.com/more/best-browser/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Product pages
        url_test("/firefox/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Product features
        url_test("/products/firefox/live-bookmarks", "https://www.firefox.com/features/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/products/firefox/search", "https://www.firefox.com/features/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        url_test("/products/firefox/switch", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test(
            "/products/firefox/system-requirements",
            "https://www.firefox.com/firefox/system-requirements/?redirect_source=mozilla-org",
            status_code=STATUS_CODE,
        ),
        url_test("/products/firefox/tabbed-browsing", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/products/firefox/upgrade", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        url_test("/products/firefox/why/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
        # Mobile
        url_test("/firefox/mobile/", "https://www.firefox.com/browsers/mobile/?redirect_source=mozilla-org", status_code=STATUS_CODE),
        # Choose
        url_test("/firefox/choose/", FXC_WITH_DEFAULT_QS, status_code=STATUS_CODE),
    )
)

# List of redirects not covered by tests:
"""
Redirects not tested:
1. mwc: redirects to support.mozilla.org/products/firefox-os
2. projects/firefox firstrun paths: redirect to internal firefox.nightly.firstrun
3. nightly/whatsnew: redirect to firefox.nightly.firstrun
4. project firefox path redirects: complex URL patterns
5. firefox/connect: redirect to mozorg.home
6. firefox/accountmanager: redirect to developer.mozilla.org/Persona
7. firefox/beta/aurora/nightly channel redirects: use platform_redirector function
8. firefox/os/(releases|notes): redirect to developer.mozilla.org
9. firefoxos: redirect to /firefox/os/
10. no_redirect for download/thanks
11. firefox/firefox.exe: redirect to mozorg.home
12. mobile/faq: uses the firefox_mobile_faq function
13. mobile/platforms: redirect to support.mozilla.org
14. firefox/releases/whatsnew redirects
15. seamonkey transition: redirect to archive.mozilla.org
16. hello survey redirects
17. firefox/customize: redirects to support.mozilla.org
18. firefox/technology: redirects to developer.mozilla.org
19. android download redirects: merge_query=True used
20. fennec projects: redirect to website-archive.mozilla.org
21. phishing protection: redirect to support.mozilla.org
22. home pages: redirect to blog.mozilla.org
23. vpat pages: redirect to website-archive.mozilla.org
24. mobile system requirements: redirect to support.mozilla.org
25. devpreview: redirects to firefox/firstrun or website-archive
26. no_redirect for certain Firefox release notes
27. mobile release notes: complex URL patterns using regex groups
28. firefox/mobile/platforms: redirect to support page
29. firefox/private-browsing: redirect to internal page
30. addon redirects: redirect to addons.mozilla.org
31. firefox/help: redirect to support.mozilla.org
32. Various project redirects to developer.mozilla.org or wiki.mozilla.org
33. firefox/org signup: more complex pattern
34. firefox/android/faq: redirect to support.mozilla.org
35. firefox/desktop/customize: redirect to support.mozilla.org
36. firefox welcome pages with version numbers
37. firefox browsers/mobile/app: uses mobile_app function
38. firefox/nothingpersonal and firefox/tech: internal redirects
39. firefox version-specific redirects
"""
