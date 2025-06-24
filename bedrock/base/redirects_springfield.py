# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from functools import partial

from django.conf import settings

from bedrock.redirects.util import not_found, redirect

FXC = getattr(settings, "FXC_BASE_URL", "https://www.firefox.com")

# All redirects in this file will get the `redirect_source` query parameter set to `mozilla-org`.
redirect = partial(redirect, query={"redirect_source": "mozilla-org"})

# Issue 16355
redirectpatterns = (
    redirect(r"^/firefox/$", FXC, permanent=True),
    redirect(r"^/firefox/browsers/$", FXC, permanent=True),
    redirect(r"^/firefox/new/$", FXC, permanent=True),
    redirect(r"^/firefox/releasenotes/$", f"{FXC}/firefox/releasenotes/", permanent=True),
    redirect(r"^/firefox/system-requirements/$", f"{FXC}/firefox/system-requirements/", permanent=True),
    redirect(r"^/firefox/all/$", f"{FXC}/download/all/", permanent=True),
    redirect(r"^/firefox/android/releasenotes/$", f"{FXC}/firefox/android/releasenotes/", permanent=True),
    redirect(r"^/firefox/android/system-requirements/$", f"{FXC}/firefox/android/system-requirements/", permanent=True),
    redirect(r"^/firefox/browsers/best-browser/$", f"{FXC}/more/best-browser/", permanent=True),
    redirect(r"^/firefox/browsers/browser-history/$", f"{FXC}/more/browser-history/", permanent=True),
    redirect(r"^/firefox/browsers/chromebook/$", f"{FXC}/browsers/desktop/chromebook/", permanent=True),
    redirect(r"^/firefox/browsers/compare/$", f"{FXC}/compare/", permanent=True),
    redirect(r"^/firefox/browsers/compare/brave/$", f"{FXC}/compare/brave/", permanent=True),
    redirect(r"^/firefox/browsers/compare/chrome/$", f"{FXC}/compare/chrome/", permanent=True),
    redirect(r"^/firefox/browsers/compare/edge/$", f"{FXC}/compare/edge/", permanent=True),
    redirect(r"^/firefox/browsers/compare/opera/$", f"{FXC}/compare/opera/", permanent=True),
    redirect(r"^/firefox/browsers/compare/safari/$", f"{FXC}/compare/safari/", permanent=True),
    redirect(r"^/firefox/browsers/incognito-browser/$", f"{FXC}/more/incognito-browser/", permanent=True),
    redirect(r"^/firefox/browsers/mobile/$", f"{FXC}/browsers/mobile/", permanent=True),
    redirect(r"^/firefox/browsers/mobile/compare/$", f"{FXC}/browsers/mobile/", permanent=True),
    redirect(r"^/firefox/browsers/mobile/android/$", f"{FXC}/browsers/mobile/android/", permanent=True),
    redirect(r"^/firefox/browsers/mobile/focus/$", f"{FXC}/browsers/mobile/focus/", permanent=True),
    redirect(r"^/firefox/browsers/mobile/ios/$", f"{FXC}/browsers/mobile/ios/", permanent=True),
    redirect(r"^/firefox/browsers/update-your-browser/$", f"{FXC}/more/update-your-browser/", permanent=True),
    redirect(r"^/firefox/browsers/what-is-a-browser/$", f"{FXC}/more/what-is-a-browser/", permanent=True),
    redirect(r"^/firefox/browsers/windows-64-bit/$", f"{FXC}/more/windows-64-bit/", permanent=True),
    # https://www.mozilla.org/en-US/firefox/channel/	redirects to /channel/{platform}	(Redirects)	redirect to /channel/{platform}		In Springfield (correct URL)		301		yes
    redirect(r"^/firefox/channel/android/$", f"{FXC}/channel/android/", permanent=True),
    redirect(r"^/firefox/channel/desktop/$", f"{FXC}/channel/desktop/", permanent=True),
    redirect(r"^/firefox/channel/ios/$", f"{FXC}/channel/ios/", permanent=True),
    redirect(r"^/firefox/developer/$", f"{FXC}/channel/desktop/developer/", permanent=True),
    redirect(r"^/firefox/download/thanks/$", f"{FXC}/thanks/", permanent=True),
    redirect(r"^/firefox/enterprise/$", f"{FXC}/browsers/enterprise/", permanent=True),
    redirect(r"^/firefox/faq/$", f"{FXC}/more/faq/", permanent=True),
    redirect(r"^/firefox/features/$", f"{FXC}/features/", permanent=True),
    redirect(r"^/firefox/features/adblocker/$", f"{FXC}/features/adblocker/", permanent=True),
    redirect(r"^/firefox/features/add-ons/$", f"{FXC}/features/add-ons/", permanent=True),
    redirect(r"^/firefox/features/block-fingerprinting/$", f"{FXC}/features/block-fingerprinting/", permanent=True),
    redirect(r"^/firefox/features/bookmarks/$", f"{FXC}/features/bookmarks/", permanent=True),
    redirect(r"^/firefox/features/customize/$", f"{FXC}/features/customize/", permanent=True),
    redirect(r"^/firefox/features/eyedropper/$", f"{FXC}/features/eyedropper/", permanent=True),
    redirect(r"^/firefox/features/fast/$", f"{FXC}/features/fast/", permanent=True),
    redirect(r"^/firefox/features/password-manager/$", f"{FXC}/features/password-manager/", permanent=True),
    redirect(r"^/firefox/features/pdf-editor/$", f"{FXC}/features/pdf-editor/", permanent=True),
    redirect(r"^/firefox/features/picture-in-picture/$", f"{FXC}/features/picture-in-picture/", permanent=True),
    redirect(r"^/firefox/features/pinned-tabs/$", f"{FXC}/features/pinned-tabs/", permanent=True),
    redirect(r"^/firefox/features/private-browsing/$", f"{FXC}/features/private-browsing/", permanent=True),
    redirect(r"^/firefox/features/private/$", f"{FXC}/features/private/", permanent=True),
    redirect(r"^/firefox/features/sync/$", f"{FXC}/features/sync/", permanent=True),
    redirect(r"^/firefox/features/tips/$", f"{FXC}/features/tips/", permanent=True),
    redirect(r"^/firefox/features/translate/$", f"{FXC}/features/translate/", permanent=True),
    redirect(r"^/firefox/installer-help/$", f"{FXC}/download/installer-help/", permanent=True),
    redirect(r"^/firefox/ios/releasenotes/$", f"{FXC}/firefox/ios/releasenotes/", permanent=True),
    redirect(r"^/firefox/ios/system-requirements/$", f"{FXC}/firefox/ios/system-requirements/", permanent=True),
    redirect(r"^/firefox/ios/testflight/$", f"{FXC}/channel/ios/testflight", permanent=True),
    redirect(r"^/firefox/linux/$", f"{FXC}/browsers/desktop/linux/", permanent=True),
    redirect(r"^/firefox/mac/$", f"{FXC}/browsers/desktop/mac/", permanent=True),
    redirect(r"^/firefox/mobile/get-app/$", f"{FXC}/browsers/mobile/get-app/", permanent=True),
    redirect(r"^/firefox/more/$", f"{FXC}/more/", permanent=True),
    redirect(r"^/firefox/releases/$", f"{FXC}/releases/", permanent=True),
    redirect(r"^/firefox/set-as-default/$", f"{FXC}/landing/set-as-default/", permanent=True),
    redirect(r"^/firefox/set-as-default/thanks/$", f"{FXC}/landing/set-as-default/thanks/", permanent=True),
    redirect(r"^/firefox/unsupported-systems/$", f"{FXC}/browsers/unsupported-systems/", permanent=True),
    redirect(r"^/firefox/windows/$", f"{FXC}/browsers/desktop/windows/", permanent=True),
    redirect(r"^/firefox/landing/get/$", f"{FXC}/landing/get", permanent=True),
    # 404s
    # TODO: Remove from here once the pages are removed from mozorg.
    not_found(r"^/firefox/browsers/compare/ie/$"),
    not_found(r"^/firefox/browsers/quantum/$"),
    not_found(r"^/firefox/facebookcontainer/$"),
    not_found(r"^/firefox/family/$"),
    not_found(r"^/firefox/flashback/$"),
    not_found(r"^/firefox/more/misinformation/$"),
    not_found(r"^/firefox/pocket/$"),
    not_found(r"^/firefox/privacy/$"),
    not_found(r"^/firefox/privacy/book/$"),
    not_found(r"^/firefox/privacy/products/$"),
    not_found(r"^/firefox/products/$"),
    not_found(r"^/firefox/switch/$"),
)
