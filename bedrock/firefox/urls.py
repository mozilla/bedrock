# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from django.conf import settings
from django.urls import path, re_path

import bedrock.releasenotes.views
from bedrock.firefox import views
from bedrock.mozorg.util import page
from bedrock.releasenotes import version_re
from bedrock.utils import views as utils_views
from bedrock.utils.views import VariationTemplateView

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
    path("firefox/", views.FirefoxHomeView.as_view(), name="firefox"),
    path("firefox/all/", views.firefox_all, name="firefox.all"),
    page("firefox/accounts/", "firefox/accounts.html", ftl_files=["firefox/accounts"]),
    page("firefox/browsers/", "firefox/browsers/index.html", ftl_files=["firefox/browsers"]),
    page("firefox/products/", "firefox/products/index.html", ftl_files=["firefox/products"]),
    page("firefox/flashback/", "firefox/flashback/index.html", active_locales=["en-US", "de", "fr"]),
    page("firefox/channel/desktop/", "firefox/channel/desktop.html", ftl_files=["firefox/channel"]),
    page("firefox/channel/android/", "firefox/channel/android.html", ftl_files=["firefox/channel"]),
    page("firefox/channel/ios/", "firefox/channel/ios.html", ftl_files=["firefox/channel"]),
    page("firefox/developer/", "firefox/developer/index.html", ftl_files=["firefox/developer"]),
    page("firefox/enterprise/", "firefox/enterprise/index.html", ftl_files=["firefox/enterprise"]),
    page("firefox/facebookcontainer/", "firefox/facebookcontainer/index.html", ftl_files=["firefox/facebook_container"]),
    page("firefox/features/", "firefox/features/index.html", ftl_files=["firefox/features/shared", "firefox/features/index"]),
    page("firefox/features/adblocker/", "firefox/features/adblocker.html", ftl_files=["firefox/features/adblocker"]),
    page("firefox/features/bookmarks/", "firefox/features/bookmarks.html", ftl_files=["firefox/features/shared", "firefox/features/bookmarks"]),
    page("firefox/features/fast/", "firefox/features/fast.html", ftl_files=["firefox/features/shared", "firefox/features/fast"]),
    page(
        "firefox/features/block-fingerprinting/",
        "firefox/features/fingerprinting.html",
        ftl_files=["firefox/features/shared", "firefox/features/fingerprinting"],
    ),
    page("firefox/features/independent/", "firefox/features/independent.html", ftl_files=["firefox/features/shared", "firefox/features/independent"]),
    page("firefox/features/memory/", "firefox/features/memory.html", ftl_files=["firefox/features/shared", "firefox/features/memory"]),
    page(
        "firefox/features/password-manager/",
        "firefox/features/password-manager.html",
        ftl_files=["firefox/features/shared", "firefox/features/password-manager"],
    ),
    page(
        "firefox/features/private-browsing/",
        "firefox/features/private-browsing.html",
        ftl_files=["firefox/features/shared", "firefox/features/private-browsing"],
    ),
    page("firefox/features/safebrowser/", "firefox/features/safebrowser.html"),
    path("firefox/features/translate/", views.firefox_features_translate, name="firefox.features.translate"),
    page(
        "firefox/features/picture-in-picture/",
        "firefox/features/picture-in-picture.html",
        ftl_files=["firefox/features/shared", "firefox/features/picture-in-picture"],
    ),
    path(
        "firefox/features/tips/",
        VariationTemplateView.as_view(
            template_name="firefox/features/tips/tips.html",
            template_context_variations=["picture-in-picture", "eyedropper", "forget"],
        ),
        name="firefox.features.tips",
    ),
    path("firefox/ios/testflight/", views.ios_testflight, name="firefox.ios.testflight"),
    path(
        "firefox/mobile/get-app/",
        VariationTemplateView.as_view(
            template_name="firefox/mobile/get-app.html", template_context_variations=["mfm", "eco-a", "eco-b", "eco-c"], ftl_files=["firefox/mobile"]
        ),
        name="firefox.mobile.get-app",
    ),
    path("firefox/send-to-device-post/", views.send_to_device_ajax, name="firefox.send-to-device-post"),
    path("firefox/sms-send-to-device-post/", views.sms_send_to_device_ajax, name="firefox.sms-send-to-device-post"),
    page("firefox/unsupported-systems/", "firefox/unsupported-systems.html"),
    path("firefox/new/", views.NewView.as_view(), name="firefox.new"),
    path("firefox/download/thanks/", views.DownloadThanksView.as_view(), name="firefox.download.thanks"),
    page("firefox/nightly/firstrun/", "firefox/nightly/firstrun.html", ftl_files=["firefox/nightly/firstrun"]),
    path("firefox/installer-help/", views.InstallerHelpView.as_view(), name="firefox.installer-help"),
    re_path(firstrun_re, views.FirstrunView.as_view(), name="firefox.firstrun"),
    re_path(whatsnew_re, views.WhatsnewView.as_view(), name="firefox.whatsnew"),
    # Release notes
    re_path(f"^firefox/(?:{platform_re}/)?(?:{channel_re}/)?notes/$", bedrock.releasenotes.views.latest_notes, name="firefox.notes"),
    path("firefox/nightly/notes/feed/", bedrock.releasenotes.views.nightly_feed, name="firefox.nightly.notes.feed"),
    re_path("firefox/(?:latest/)?releasenotes/$", bedrock.releasenotes.views.latest_notes, {"product": "firefox"}),
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
    page("firefox/welcome/2/", "firefox/welcome/page2.html", ftl_files=["firefox/welcome/page2"]),
    page("firefox/welcome/3/", "firefox/welcome/page3.html", ftl_files=["firefox/welcome/page3"]),
    page("firefox/welcome/4/", "firefox/welcome/page4.html", ftl_files=["firefox/welcome/page4"]),
    page("firefox/welcome/6/", "firefox/welcome/page6.html", ftl_files=["firefox/welcome/page6"]),
    page("firefox/welcome/7/", "firefox/welcome/page7.html", ftl_files=["firefox/welcome/page7"]),
    path(
        "firefox/welcome/8/",
        utils_views.VariationTemplateView.as_view(
            template_name="firefox/welcome/page8.html",
            ftl_files=["firefox/welcome/page8"],
            template_context_variations=["text", "image", "animation", "header-text"],
            variation_locales=["en-US", "en-CA", "en-GB", "de", "fr"],
        ),
        name="firefox.welcome.page8",
    ),
    page("firefox/welcome/9/", "firefox/welcome/page9.html", active_locales=["de", "fr"]),
    page("firefox/welcome/10/", "firefox/welcome/page10.html", ftl_files=["firefox/welcome/page10"]),
    page("firefox/welcome/11/", "firefox/welcome/page11.html", ftl_files=["firefox/welcome/page11"]),
    page("firefox/welcome/12/", "firefox/welcome/page12.html", active_locales=["en-US", "en-CA", "en-GB"]),
    page("firefox/welcome/13/", "firefox/welcome/page13.html", ftl_files=["firefox/welcome/page13"]),
    page("firefox/switch/", "firefox/switch.html", ftl_files=["firefox/switch"]),
    page("firefox/pocket/", "firefox/pocket.html"),
    # Issue 6604, SEO firefox/new pages
    path("firefox/linux/", views.PlatformViewLinux.as_view(), name="firefox.linux"),
    path("firefox/mac/", views.PlatformViewMac.as_view(), name="firefox.mac"),
    path("firefox/windows/", views.PlatformViewWindows.as_view(), name="firefox.windows"),
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
        "firefox/browsers/compare/ie/",
        "firefox/browsers/compare/ie.html",
        ftl_files=["firefox/browsers/compare/ie", "firefox/browsers/compare/shared"],
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
    # Issue 10182
    path("firefox/browsers/mobile/", views.FirefoxMobileView.as_view(), name="firefox.browsers.mobile.index"),
    path(
        "firefox/browsers/mobile/android/",
        VariationTemplateView.as_view(
            template_name="firefox/browsers/mobile/android.html",
            template_context_variations=["1", "2", "3"],
            variation_locales=["en-US"],
            ftl_files=["firefox/browsers/mobile/android"],
        ),
        name="firefox.browsers.mobile.android",
    ),
    page("firefox/browsers/mobile/ios/", "firefox/browsers/mobile/ios.html", ftl_files=["firefox/browsers/mobile/ios"]),
    page("firefox/browsers/mobile/focus/", "firefox/browsers/mobile/focus.html", ftl_files=["firefox/browsers/mobile/focus"]),
    page(
        "firefox/browsers/mobile/compare/",
        "firefox/browsers/mobile/compare.html",
        ftl_files=["firefox/browsers/mobile/compare", "firefox/browsers/compare/shared"],
    ),
    # Issue 8641
    page("firefox/browsers/best-browser/", "firefox/browsers/best-browser.html", ftl_files=["firefox/browsers/best-browser"]),
    page("firefox/browsers/browser-history/", "firefox/browsers/browser-history.html", ftl_files=["firefox/browsers/history/browser-history"]),
    page("firefox/browsers/incognito-browser/", "firefox/browsers/incognito-browser.html"),
    page("firefox/browsers/update-your-browser/", "firefox/browsers/update-browser.html"),
    page("firefox/browsers/what-is-a-browser/", "firefox/browsers/what-is-a-browser.html", ftl_files=["firefox/browsers/history/what-is-a-browser"]),
    page("firefox/browsers/windows-64-bit/", "firefox/browsers/windows-64-bit.html", ftl_files=["firefox/browsers/windows-64-bit"]),
    # Issue 7765, 7709
    page("firefox/privacy/", "firefox/privacy/index.html", ftl_files=["firefox/privacy-hub"]),
    page("firefox/privacy/products/", "firefox/privacy/products.html", ftl_files=["firefox/privacy-hub"]),
    page("firefox/privacy/safe-passwords/", "firefox/privacy/passwords.html", ftl_files=["firefox/privacy-hub", "firefox/privacy/passwords"]),
    # Issue 8432
    page("firefox/set-as-default/thanks/", "firefox/set-as-default/thanks.html", ftl_files="firefox/set-as-default/thanks"),
    # Default browser campaign
    path(
        "firefox/set-as-default/",
        VariationTemplateView.as_view(
            template_name="firefox/set-as-default/landing.html",
            ftl_files="firefox/set-as-default/landing",
            variation_locales=["en-US"],
            template_context_variations=["1", "2", "3"],
        ),
        name="firefox.set-as-default",
    ),
    # Issue #9490 - Evergreen Content for SEO
    page("firefox/more/", "firefox/more.html", ftl_files="firefox/more"),
    page("firefox/browsers/quantum/", "firefox/browsers/quantum.html", ftl_files="firefox/browsers/quantum"),
    page("firefox/faq/", "firefox/faq.html", ftl_files="firefox/faq"),
    page("firefox/browsers/chromebook/", "firefox/browsers/chromebook.html", ftl_files="firefox/browsers/chromebook"),
    page("firefox/sync/", "firefox/sync.html", ftl_files="firefox/sync"),
    page("firefox/privacy/book/", "firefox/privacy/book.html", ftl_files="firefox/privacy/book"),
    # Issue 9957
    page("firefox/more/misinformation/", "firefox/more/misinformation.html", ftl_files="firefox/more/misinformation"),
    # Firefox for Families evergreen page, Issue #12004
    page("firefox/family/", "firefox/family/index.html"),
)

# Contentful
if settings.DEV:
    urlpatterns += (path("firefox/more/<content_id>/", views.FirefoxContenful.as_view()),)
