# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.urls import path, re_path

import bedrock.releasenotes.views
from bedrock.firefox import views
from bedrock.mozorg.util import page
from bedrock.releasenotes import version_re
from bedrock.utils.views import VariationTemplateView

# Note that these regular expressions are also used in bedrock.firefox.redirects,
# so if they become redundant here, they will need to be moved to that module.
latest_re = r"^firefox(?:/(?P<version>%s))?/%s/$"
firstrun_re = latest_re % (version_re, "firstrun")
whatsnew_re = latest_re % (version_re, "whatsnew")
platform_re = "(?P<platform>android|ios)"
channel_re = "(?P<channel>beta|aurora|developer|nightly|organizations)"
releasenotes_re = latest_re % (version_re, r"(aurora|release)notes")
android_releasenotes_re = releasenotes_re.replace(r"firefox", "firefox/android")
ios_releasenotes_re = releasenotes_re.replace(r"firefox", "firefox/ios")
sysreq_re = latest_re % (version_re, "system-requirements")
android_sysreq_re = sysreq_re.replace(r"firefox", "firefox/android")
ios_sysreq_re = sysreq_re.replace(r"firefox", "firefox/ios")


urlpatterns = (
    path(
        "firefox/challenge-the-default/",
        VariationTemplateView.as_view(
            template_name="firefox/challenge-the-default/landing-switch.html",
            active_locales=["de", "es-ES", "fr", "it", "pl"],
            variation_locales=["de", "fr"],
            template_context_variations=["1", "2", "3", "4", "5", "6"],
        ),
    ),
    path("firefox/all/", views.firefox_all, name="firefox.all"),
    path("firefox/all/<slug:product_slug>/", views.firefox_all, name="firefox.all.platforms"),
    path("firefox/all/<slug:product_slug>/<str:platform>/", views.firefox_all, name="firefox.all.locales"),
    path("firefox/all/<slug:product_slug>/<str:platform>/<str:locale>/", views.firefox_all, name="firefox.all.download"),
    page("firefox/channel/desktop/", "firefox/channel/desktop.html", ftl_files=["firefox/channel"]),
    page("firefox/channel/android/", "firefox/channel/android.html", ftl_files=["firefox/channel"]),
    page("firefox/channel/ios/", "firefox/channel/ios.html", ftl_files=["firefox/channel"]),
    page("firefox/developer/", "firefox/developer/index.html", ftl_files=["firefox/developer"]),
    page("firefox/enterprise/", "firefox/enterprise/index.html", ftl_files=["firefox/enterprise"]),
    page("firefox/facebookcontainer/", "firefox/facebookcontainer/index.html", ftl_files=["firefox/facebook_container"]),
    page("firefox/features/", "firefox/features/index.html", ftl_files=["firefox/features/index-2023", "firefox/features/shared"]),
    page("firefox/features/customize/", "firefox/features/customize.html", ftl_files=["firefox/features/customize-2023", "firefox/features/shared"]),
    page("firefox/features/add-ons/", "firefox/features/add-ons.html", ftl_files=["firefox/features/add-ons-2023", "firefox/features/shared"]),
    page(
        "firefox/features/pinned-tabs/",
        "firefox/features/pinned-tabs.html",
        ftl_files=["firefox/features/pinned-tabs-2023", "firefox/features/shared"],
    ),
    page(
        "firefox/features/eyedropper/", "firefox/features/eyedropper.html", ftl_files=["firefox/features/eyedropper-2023", "firefox/features/shared"]
    ),
    path("firefox/features/pdf-editor/", views.firefox_features_pdf.as_view(), name="firefox.features.pdf-editor"),
    path("firefox/features/adblocker/", views.firefox_features_adblocker.as_view(), name="firefox.features.adblocker"),
    page("firefox/features/bookmarks/", "firefox/features/bookmarks.html", ftl_files=["firefox/features/bookmarks-2023", "firefox/features/shared"]),
    path("firefox/features/fast/", views.firefox_features_fast.as_view(), name="firefox.features.fast"),
    page(
        "firefox/features/block-fingerprinting/",
        "firefox/features/fingerprinting.html",
        ftl_files=["firefox/features/fingerprinting", "firefox/features/shared"],
    ),
    page(
        "firefox/features/password-manager/",
        "firefox/features/password-manager.html",
        ftl_files=["firefox/features/password-manager-2023", "firefox/features/shared"],
    ),
    page(
        "firefox/features/private/",
        "firefox/features/private.html",
        ftl_files=["firefox/features/private-2023", "firefox/features/shared"],
    ),
    page(
        "firefox/features/private-browsing/",
        "firefox/features/private-browsing.html",
        ftl_files=["firefox/features/private-browsing-2023", "firefox/features/shared"],
    ),
    page("firefox/features/sync/", "firefox/features/sync.html", ftl_files=["firefox/features/sync-2023", "firefox/features/shared"]),
    path("firefox/features/translate/", views.firefox_features_translate, name="firefox.features.translate"),
    page(
        "firefox/features/picture-in-picture/",
        "firefox/features/picture-in-picture.html",
        ftl_files=["firefox/features/picture-in-picture", "firefox/features/shared"],
    ),
    path(
        "firefox/features/tips/",
        VariationTemplateView.as_view(
            template_name="firefox/features/tips/tips.html",
            template_context_variations=["picture-in-picture", "eyedropper", "forget"],
        ),
        name="firefox.features.tips",
    ),
    path(
        "firefox/features/complete-pdf/",
        VariationTemplateView.as_view(
            template_name="firefox/features/pdf-complete-fr.html", ftl_files=["firefox/features/shared"], active_locales=["fr"]
        ),
        name="firefox.features.pdf-complete",
    ),
    path(
        "firefox/features/free-pdf-editor/",
        VariationTemplateView.as_view(
            template_name="firefox/features/pdf-free-fr.html", ftl_files=["firefox/features/shared"], active_locales=["fr"]
        ),
        name="firefox.features.pdf-free",
    ),
    path("firefox/ios/testflight/", views.ios_testflight, name="firefox.ios.testflight"),
    page("firefox/unsupported-systems/", "firefox/unsupported-systems.html"),
    path("firefox/download/thanks/", views.DownloadThanksView.as_view(), name="firefox.download.thanks"),
    page("firefox/nightly/firstrun/", "firefox/nightly/firstrun.html", ftl_files=["firefox/nightly/firstrun"]),
    path("firefox/installer-help/", views.InstallerHelpView.as_view(), name="firefox.installer-help"),
    re_path(firstrun_re, views.FirstrunView.as_view(), name="firefox.firstrun"),
    re_path(whatsnew_re, views.WhatsnewView.as_view(), name="firefox.whatsnew"),
    # Release notes
    re_path(f"^firefox/(?:{platform_re}/)?(?:{channel_re}/)?notes/$", bedrock.releasenotes.views.latest_notes, name="firefox.notes"),
    path("firefox/nightly/notes/feed/", bedrock.releasenotes.views.nightly_feed, name="firefox.nightly.notes.feed"),
    re_path("firefox/(?:latest/)?releasenotes/$", bedrock.releasenotes.views.latest_notes, {"product": "firefox"}),
    path("firefox/android/releasenotes/", bedrock.releasenotes.views.latest_notes, {"product": "Firefox for Android"}),
    path("firefox/ios/releasenotes/", bedrock.releasenotes.views.latest_notes, {"product": "Firefox for iOS"}),
    re_path(
        f"^firefox/(?:{platform_re}/)?(?:{channel_re}/)?system-requirements/$",
        bedrock.releasenotes.views.latest_sysreq,
        {"product": "firefox"},
        name="firefox.sysreq",
    ),
    re_path(releasenotes_re, bedrock.releasenotes.views.release_notes, name="firefox.desktop.releasenotes"),
    re_path(
        android_releasenotes_re, bedrock.releasenotes.views.release_notes, {"product": "Firefox for Android"}, name="firefox.android.releasenotes"
    ),
    re_path(ios_releasenotes_re, bedrock.releasenotes.views.release_notes, {"product": "Firefox for iOS"}, name="firefox.ios.releasenotes"),
    re_path(sysreq_re, bedrock.releasenotes.views.system_requirements, name="firefox.system_requirements"),
    re_path(
        android_sysreq_re,
        bedrock.releasenotes.views.system_requirements,
        {"product": "Firefox for Android"},
        name="firefox.android.system_requirements",
    ),
    re_path(ios_sysreq_re, bedrock.releasenotes.views.system_requirements, {"product": "Firefox for iOS"}, name="firefox.ios.system_requirements"),
    path("firefox/releases/", bedrock.releasenotes.views.releases_index, {"product": "Firefox"}, name="firefox.releases.index"),
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
    page("firefox/nothing-personal/", "firefox/nothing-personal/index.html"),
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
    page(
        "firefox/browsers/compare/",
        "firefox/browsers/compare/index.html",
        ftl_files=["firefox/browsers/compare/index", "firefox/browsers/compare/shared"],
    ),
    page(
        "firefox/browsers/compare/brave/",
        "firefox/browsers/compare/brave.html",
        ftl_files=["firefox/browsers/compare/brave", "firefox/browsers/compare/shared"],
    ),
    page(
        "firefox/browsers/compare/chrome/",
        "firefox/browsers/compare/chrome.html",
        ftl_files=["firefox/browsers/compare/chrome", "firefox/browsers/compare/shared"],
    ),
    page(
        "firefox/browsers/compare/edge/",
        "firefox/browsers/compare/edge.html",
        ftl_files=["firefox/browsers/compare/edge", "firefox/browsers/compare/shared"],
    ),
    page(
        "firefox/browsers/compare/opera/",
        "firefox/browsers/compare/opera.html",
        ftl_files=["firefox/browsers/compare/opera", "firefox/browsers/compare/shared"],
    ),
    page(
        "firefox/browsers/compare/safari/",
        "firefox/browsers/compare/safari.html",
        ftl_files=["firefox/browsers/compare/safari", "firefox/browsers/compare/shared"],
    ),
    # Issue 8432
    # Issue 13253: Ensure that Firefox can continue to refer to this URL.
    page("firefox/set-as-default/thanks/", "firefox/set-as-default/thanks.html", ftl_files="firefox/set-as-default/thanks"),
    # Default browser campaign
    page("firefox/set-as-default/", "firefox/set-as-default/landing.html", ftl_files="firefox/set-as-default/landing"),
    # Issue #9490 - Evergreen Content for SEO
    page("firefox/more/", "firefox/more.html", ftl_files="firefox/more"),
    page("firefox/browsers/quantum/", "firefox/browsers/quantum.html", ftl_files="firefox/browsers/quantum"),
    page("firefox/faq/", "firefox/faq.html", ftl_files="firefox/faq"),
    page("firefox/browsers/chromebook/", "firefox/browsers/chromebook.html", ftl_files="firefox/browsers/chromebook"),
    # Issue 9957
    page("firefox/more/misinformation/", "firefox/more/misinformation.html", ftl_files="firefox/more/misinformation"),
    # Firefox for Families evergreen page, Issue #12004
    page("firefox/family/", "firefox/family/index.html"),
    # Issue 14985 - "Built For You" campaign landing page
    path(
        "firefox/built-for-you/",
        VariationTemplateView.as_view(
            template_name="firefox/built-for-you/landing.html",
            active_locales=["de", "fr"],
            variation_locales=["de", "fr"],
            template_context_variations=["1", "2", "3", "4", "5"],
        ),
    ),
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
