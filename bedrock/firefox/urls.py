# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.urls import path, re_path

from bedrock.firefox import version_re, views
from bedrock.mozorg.util import page

# `latest_re`, `version_re`, `platform_re` and `channel_re` are also imported by
# bedrock.firefox.redirects to build the release-notes / system-requirements
# redirect patterns, so keep them defined here.
latest_re = r"^firefox(?:/(?P<version>%s))?/%s/$"
firstrun_re = latest_re % (version_re, "firstrun")
whatsnew_re = latest_re % (version_re, "whatsnew")
platform_re = "(?P<platform>android|ios)"
channel_re = "(?P<channel>beta|aurora|developer|nightly|organizations)"


urlpatterns = (
    path("firefox/all/", views.firefox_all, name="firefox.all"),
    path("firefox/all/<slug:product_slug>/", views.firefox_all, name="firefox.all.platforms"),
    path("firefox/all/<slug:product_slug>/<str:platform>/", views.firefox_all, name="firefox.all.locales"),
    path("firefox/all/<slug:product_slug>/<str:platform>/<str:locale>/", views.firefox_all, name="firefox.all.download"),
    # Channel, enterprise, features, and set-as-default pages are now served by
    # www.firefox.com. The rendering views have been removed; RedirectsMiddleware
    # (see bedrock.firefox.redirects) 301s every path to www.firefox.com. These
    # named routes are retained — pointing at a fallback redirect view — purely so
    # templates that still link to them remain reversible.
    path("firefox/channel/desktop/", views.fxc_redirect, name="firefox.channel.desktop"),
    path("firefox/channel/android/", views.fxc_redirect, name="firefox.channel.android"),
    path("firefox/channel/ios/", views.fxc_redirect, name="firefox.channel.ios"),
    page("firefox/developer/", "firefox/developer/index.html", ftl_files=["firefox/developer"]),
    path("firefox/enterprise/", views.fxc_redirect, name="firefox.enterprise.index"),
    path("firefox/facebookcontainer/", views.fxc_redirect, name="firefox.facebookcontainer.index"),
    path("firefox/features/", views.fxc_redirect, name="firefox.features.index"),
    path("firefox/features/pdf-editor/", views.fxc_redirect, name="firefox.features.pdf-editor"),
    path("firefox/features/adblocker/", views.fxc_redirect, name="firefox.features.adblocker"),
    path("firefox/features/fast/", views.fxc_redirect, name="firefox.features.fast"),
    path("firefox/features/block-fingerprinting/", views.fxc_redirect, name="firefox.features.fingerprinting"),
    path("firefox/features/password-manager/", views.fxc_redirect, name="firefox.features.password-manager"),
    path("firefox/features/private/", views.fxc_redirect, name="firefox.features.private"),
    path("firefox/features/private-browsing/", views.fxc_redirect, name="firefox.features.private-browsing"),
    path("firefox/features/sync/", views.fxc_redirect, name="firefox.features.sync"),
    path("firefox/features/translate/", views.fxc_redirect, name="firefox.features.translate"),
    path("firefox/features/picture-in-picture/", views.fxc_redirect, name="firefox.features.picture-in-picture"),
    path("firefox/features/tips/", views.fxc_redirect, name="firefox.features.tips"),
    path("firefox/ios/testflight/", views.ios_testflight, name="firefox.ios.testflight"),
    page("firefox/unsupported-systems/", "firefox/unsupported-systems.html"),
    path("firefox/download/thanks/", views.DownloadThanksView.as_view(), name="firefox.download.thanks"),
    page("firefox/nightly/firstrun/", "firefox/nightly/firstrun.html", ftl_files=["firefox/nightly/firstrun"]),
    path("firefox/installer-help/", views.InstallerHelpView.as_view(), name="firefox.installer-help"),
    re_path(firstrun_re, views.FirstrunView.as_view(), name="firefox.firstrun"),
    re_path(whatsnew_re, views.WhatsnewView.as_view(), name="firefox.whatsnew"),
    # Release notes and system requirements pages are now served by www.firefox.com.
    # The rendering views have been removed; RedirectsMiddleware (see
    # bedrock.firefox.redirects) 301s every release-notes / system-requirements path
    # to www.firefox.com. These named routes are retained — pointing at a fallback
    # redirect view — purely so templates that still link to them remain reversible.
    re_path(f"^firefox/(?:{platform_re}/)?(?:{channel_re}/)?notes/$", views.releasenotes_redirect, name="firefox.notes"),
    re_path(f"^firefox/(?:{platform_re}/)?(?:{channel_re}/)?system-requirements/$", views.releasenotes_redirect, name="firefox.sysreq"),
    path("firefox/releases/", views.releasenotes_redirect, name="firefox.releases.index"),
    path("firefox/stub_attribution_code/", views.stub_attribution_code, name="firefox.stub_attribution_code"),
    path("firefox/welcome/1/", views.firefox_welcome_page1, name="firefox.welcome.page1"),
    page("firefox/welcome/4/", "firefox/welcome/page4.html", ftl_files=["firefox/welcome/page4"]),
    page("firefox/welcome/6/", "firefox/welcome/page6.html", ftl_files=["firefox/welcome/page6"]),
    page("firefox/welcome/7/", "firefox/welcome/page7.html", ftl_files=["firefox/welcome/page7"]),
    page("firefox/welcome/8/", "firefox/welcome/page8.html", ftl_files=["firefox/welcome/page8"]),
    page("firefox/welcome/9/", "firefox/welcome/page9.html", active_locales=["de", "fr"]),
    page("firefox/welcome/10/", "firefox/welcome/page10.html", ftl_files=["firefox/welcome/page10"]),
    page("firefox/welcome/11/", "firefox/welcome/page11.html", ftl_files=["firefox/welcome/page11"]),
    page("firefox/welcome/12/", "firefox/welcome/page12.html", active_locales=["en-US", "en-CA", "en-GB"]),
    page("firefox/welcome/13/", "firefox/welcome/page13.html", ftl_files=["firefox/welcome/page13"]),
    page("firefox/welcome/14/", "firefox/welcome/page14.html", ftl_files=["firefox/welcome/page14"]),
    page("firefox/welcome/15/", "firefox/welcome/page15.html", active_locales=["en-US", "en-CA", "en-GB", "fr", "de"]),
    page("firefox/welcome/16/", "firefox/welcome/page16.html"),
    page("firefox/welcome/17a/", "firefox/welcome/page17/page17-a.html", ftl_files=["firefox/welcome/page14"], active_locales=["en-US", "fr", "de"]),
    page("firefox/welcome/17b/", "firefox/welcome/page17/page17-b.html", ftl_files=["firefox/welcome/page14"], active_locales=["en-US", "fr", "de"]),
    page("firefox/welcome/17c/", "firefox/welcome/page17/page17-c.html", ftl_files=["firefox/welcome/page14"], active_locales=["en-US", "fr", "de"]),
    page(
        "firefox/welcome/19/",
        "firefox/welcome/page19.html",
        active_locales=[
            "en-US",
            "ar",
            "cs",
            "de",
            "el",
            "es-ES",
            "fr",
            "hu",
            "id",
            "it",
            "ja",
            "pl",
            "pt-BR",
            "ru",
            "zh-CN",
        ],
    ),
    page("firefox/welcome/20/", "firefox/welcome/page20.html", ftl_files=["firefox/welcome/page20-21"]),
    page("firefox/welcome/21/", "firefox/welcome/page21.html", ftl_files=["firefox/welcome/page20-21"]),
    page("firefox/welcome/22/", "firefox/welcome/page22.html", ftl_files=["firefox/welcome/page22"]),
    page("firefox/welcome/23/", "firefox/welcome/page23.html", ftl_files=["firefox/welcome/page23"]),
    page("firefox/welcome/24/", "firefox/welcome/page24.html", ftl_files=["firefox/welcome/page24"]),
    page("firefox/welcome/25/", "firefox/welcome/page25.html", active_locales=["en-US", "fr", "de"]),
    page(
        "firefox/welcome/26/",
        "firefox/welcome/page26.html",
        active_locales=["en-US", "en-CA", "en-GB", "fr", "de", "pt-BR", "pt-PT", "ja", "es-AR", "es-CL", "es-ES", "es-MX", "pl", "it"],
    ),
    page("firefox/switch/", "firefox/switch.html", ftl_files=["firefox/switch"]),
    page("firefox/share/", "firefox/share.html", active_locales=["de", "fr", "en-US", "en-CA"]),
    path("firefox/nothing-personal/", views.fxc_redirect, name="firefox.nothing-personal.index"),
    # Issue 6604, SEO firefox/new pages
    path("firefox/linux/", views.PlatformViewLinux.as_view(), name="firefox.linux"),
    path("firefox/mac/", views.PlatformViewMac.as_view(), name="firefox.mac"),
    path("firefox/windows/", views.PlatformViewWindows.as_view(), name="firefox.windows"),
    # Issue 10182
    page("firefox/browsers/mobile/", "firefox/browsers/mobile/index.html", ftl_files=["firefox/browsers/mobile/index"]),
    page("firefox/browsers/mobile/android/", "firefox/browsers/mobile/android.html", ftl_files=["firefox/browsers/mobile/android"]),
    page("firefox/browsers/mobile/ios/", "firefox/browsers/mobile/ios.html", ftl_files=["firefox/browsers/mobile/ios"]),
    page("firefox/browsers/mobile/get-ios/", "firefox/browsers/mobile/get-ios.html", ftl_files=["firefox/browsers/mobile/get-ios"]),
    page("firefox/browsers/mobile/focus/", "firefox/browsers/mobile/focus.html", ftl_files=["firefox/browsers/mobile/focus"]),
    page("firefox/browsers/mobile/get-app/", "firefox/browsers/mobile/get-app.html", ftl_files=["firefox/mobile"]),
    # Issue 8641
    page("firefox/browsers/best-browser/", "firefox/browsers/best-browser.html", ftl_files=["firefox/browsers/best-browser"]),
    page("firefox/browsers/browser-history/", "firefox/browsers/browser-history.html", ftl_files=["firefox/browsers/history/browser-history"]),
    page("firefox/browsers/incognito-browser/", "firefox/browsers/incognito-browser.html"),
    page("firefox/browsers/update-your-browser/", "firefox/browsers/update-browser.html"),
    page("firefox/browsers/what-is-a-browser/", "firefox/browsers/what-is-a-browser.html", ftl_files=["firefox/browsers/history/what-is-a-browser"]),
    page("firefox/browsers/windows-64-bit/", "firefox/browsers/windows-64-bit.html", ftl_files=["firefox/browsers/windows-64-bit"]),
    # These pages are now served by www.firefox.com; named routes are retained so
    # templates that still link to them remain reversible.
    path("firefox/browsers/compare/", views.fxc_redirect, name="firefox.browsers.compare.index"),
    path("firefox/browsers/compare/brave/", views.fxc_redirect, name="firefox.browsers.compare.brave"),
    path("firefox/browsers/compare/chrome/", views.fxc_redirect, name="firefox.browsers.compare.chrome"),
    path("firefox/browsers/compare/edge/", views.fxc_redirect, name="firefox.browsers.compare.edge"),
    path("firefox/browsers/compare/opera/", views.fxc_redirect, name="firefox.browsers.compare.opera"),
    path("firefox/browsers/compare/safari/", views.fxc_redirect, name="firefox.browsers.compare.safari"),
    # Issue 8432
    # Issue 13253: Ensure that Firefox can continue to refer to this URL.
    # These pages are now served by www.firefox.com; named routes are retained so
    # templates that still link to them remain reversible.
    path("firefox/set-as-default/thanks/", views.fxc_redirect, name="firefox.set-as-default.thanks"),
    path("firefox/set-as-default/", views.fxc_redirect, name="firefox.set-as-default.landing"),
    # Issue #9490 - Evergreen Content for SEO
    page("firefox/browsers/quantum/", "firefox/browsers/quantum.html", ftl_files="firefox/browsers/quantum"),
    page("firefox/faq/", "firefox/faq.html", ftl_files="firefox/faq"),
    page("firefox/browsers/chromebook/", "firefox/browsers/chromebook.html", ftl_files="firefox/browsers/chromebook"),
    # These pages are now served by www.firefox.com; named routes are retained so
    # templates that still link to them remain reversible.
    path("firefox/family/", views.fxc_redirect, name="firefox.family.index"),
    # Issue 15383 - Firefox 20th landing page
    page(
        "firefox/firefox20/",
        "firefox/firefox-20th/index.html",
        active_locales=["de", "fr", "en-US", "en-CA", "en-GB"],
    ),
    # Issue 15841, 15920, 5953 - UK influencer campaign pages
    page("firefox/landing/tech/", "firefox/landing/tech.html", ftl_files="firefox/new/desktop", active_locales="en-GB"),
    page("firefox/landing/education/", "firefox/landing/education.html", ftl_files="firefox/new/desktop", active_locales="en-GB"),
    page("firefox/landing/gaming/", "firefox/landing/gaming.html", ftl_files="firefox/new/desktop", active_locales="en-GB"),
    page("firefox/landing/get/", "firefox/landing/get.html", ftl_files="firefox/new/desktop"),
)
