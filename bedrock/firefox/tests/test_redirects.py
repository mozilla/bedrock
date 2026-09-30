# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch
from urllib.parse import parse_qsl, urlparse

from django.conf import settings
from django.http import Http404
from django.test import RequestFactory

import pytest

from bedrock.firefox.redirects import mobile_app, validate_param_value
from bedrock.firefox.views import (
    FIREFOX_ALL_PLATFORM_MAP,
    FIREFOX_ALL_PRODUCTS,
    firefox_all,
    fxc_redirect,
    releasenotes_redirect,
)
from bedrock.redirects.util import mobile_app_redirector

ANDROID_UA = "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36"
IOS_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"


@pytest.mark.parametrize(
    "test_param, is_valid",
    (
        ("firefox-whatsnew", True),
        ("firefox-welcome-4", True),
        ("firefox-welcome-6", True),
        ("firefox-welcome-17-en", True),
        ("firefox-welcome-17-de", True),
        ("firefox-welcome-17-fr", True),
        ("firefox-browsers-mobile-get-app", True),
        ("firefox-browsers-mobile-focus", True),
        ("mzaonboardingemail-de", True),
        ("mzaonboardingemail-fr", True),
        ("mzaonboardingemail-es", True),
        ("firefox-all", True),
        ("fxshare1", True),
        ("fxshare2", True),
        ("fxshare3", True),
        ("fxshare4", True),
        ("fxshare12", True),
        ("fxshare14", True),
        ("fxshare15", True),
        ("DESKTOP_FEATURE_CALLOUT_SIGNED_INTO_ACCOUNT.treatment_a", True),
        ("DESKTOP_FEATURE_CALLOUT_SIGNED_INTO_ACCOUNT.treatment_b", True),
        ("wnp134-de-a", True),
        ("wnp134-de-b", True),
        ("wnp134-de-c", True),
        ("wnp134-en-ca-a", True),
        ("wnp134-en-ca-b", True),
        ("smi-marvintsp", True),
        ("smi-koschtaaa", True),
        ("smi-bytereview", True),
        ("pocket-test", True),
        ("some<nefarious$thing", False),
        ("ano+h3r=ne", False),
        ("ǖnicode", False),
        ("♪♫♬♭♮♯", False),
        ("", False),
        (None, False),
    ),
)
def test_param_verification(test_param, is_valid):
    if is_valid:
        assert validate_param_value(test_param) == test_param
    else:
        assert validate_param_value(test_param) is None


def test_mobile_app():
    rf = RequestFactory()

    # both args exist and have valid values
    req = rf.get("/firefox/app/?product=focus&campaign=firefox-all")
    with patch("bedrock.firefox.redirects.mobile_app_redirector") as mar:
        mobile_app(req)
        mar.assert_called_with(req, "focus", "firefox-all")

    # neither args exist
    req = rf.get("/firefox/app/")
    with patch("bedrock.firefox.redirects.mobile_app_redirector") as mar:
        mobile_app(req)
        mar.assert_called_with(req, "firefox", None)

    # both args exist but invalid values
    req = rf.get("/firefox/app/?product=dude&campaign=walter$")
    with patch("bedrock.firefox.redirects.mobile_app_redirector") as mar:
        mobile_app(req)
        mar.assert_called_with(req, "firefox", None)

    # other args exist
    req = rf.get("/firefox/app/?bunny=dude&maude=artist")
    with patch("bedrock.firefox.redirects.mobile_app_redirector") as mar:
        mobile_app(req)
        mar.assert_called_with(req, "firefox", None)


EXPECTED_REDIRECT_QS = "?redirect_source=mozilla-org"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,expected_location,expected_status,follow_redirects",
    [
        (
            "/en-US/firefox/",
            f"{settings.FXC_BASE_URL}/en-US/{EXPECTED_REDIRECT_QS}",
            200,
            True,
        ),
        (
            "/en-US/firefox/new/",
            f"{settings.FXC_BASE_URL}/en-US/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/all/",
            f"{settings.FXC_BASE_URL}/en-US/download/all/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/installer-help/",
            f"{settings.FXC_BASE_URL}/en-US/download/installer-help/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/",
            f"{settings.FXC_BASE_URL}/en-US/{EXPECTED_REDIRECT_QS}",
            200,
            True,
        ),
        (
            "/en-US/firefox/browsers/best-browser/",
            f"{settings.FXC_BASE_URL}/en-US/more/best-browser/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/browser-history/",
            f"{settings.FXC_BASE_URL}/en-US/more/browser-history/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/chromebook/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/desktop/chromebook/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/",
            f"{settings.FXC_BASE_URL}/en-US/compare/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/brave/",
            f"{settings.FXC_BASE_URL}/en-US/compare/brave/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/chrome/",
            f"{settings.FXC_BASE_URL}/en-US/compare/chrome/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/edge/",
            f"{settings.FXC_BASE_URL}/en-US/compare/edge/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/opera/",
            f"{settings.FXC_BASE_URL}/en-US/compare/opera/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/safari/",
            f"{settings.FXC_BASE_URL}/en-US/compare/safari/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/incognito-browser/",
            f"{settings.FXC_BASE_URL}/en-US/more/incognito-browser/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/mobile/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/android/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/mobile/android/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/focus/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/mobile/focus/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/ios/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/mobile/ios/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/update-your-browser/",
            f"{settings.FXC_BASE_URL}/en-US/more/update-your-browser/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/what-is-a-browser/",
            f"{settings.FXC_BASE_URL}/en-US/more/what-is-a-browser/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/browsers/windows-64-bit/",
            f"{settings.FXC_BASE_URL}/en-US/more/windows-64-bit/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/channel/android/",
            f"{settings.FXC_BASE_URL}/en-US/channel/android/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/channel/desktop/",
            f"{settings.FXC_BASE_URL}/en-US/channel/desktop/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/channel/ios/",
            f"{settings.FXC_BASE_URL}/en-US/channel/ios/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/developer/",
            f"{settings.FXC_BASE_URL}/en-US/channel/desktop/developer/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/enterprise/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/enterprise/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/faq/",
            f"{settings.FXC_BASE_URL}/en-US/more/faq/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/",
            f"{settings.FXC_BASE_URL}/en-US/features/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/adblocker/",
            f"{settings.FXC_BASE_URL}/en-US/features/adblocker/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/add-ons/",
            f"{settings.FXC_BASE_URL}/en-US/features/add-ons/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/block-fingerprinting/",
            f"{settings.FXC_BASE_URL}/en-US/features/block-fingerprinting/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/bookmarks/",
            f"{settings.FXC_BASE_URL}/en-US/features/bookmarks/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/fr/firefox/features/complete-pdf/",
            f"{settings.FXC_BASE_URL}/fr/features/complete-pdf/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/customize/",
            f"{settings.FXC_BASE_URL}/en-US/features/customize/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/eyedropper/",
            f"{settings.FXC_BASE_URL}/en-US/features/eyedropper/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/fast/",
            f"{settings.FXC_BASE_URL}/en-US/features/fast/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/fr/firefox/features/free-pdf-editor/",
            f"{settings.FXC_BASE_URL}/fr/features/free-pdf-editor/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/password-manager/",
            f"{settings.FXC_BASE_URL}/en-US/features/password-manager/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/pdf-editor/",
            f"{settings.FXC_BASE_URL}/en-US/features/pdf-editor/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/picture-in-picture/",
            f"{settings.FXC_BASE_URL}/en-US/features/picture-in-picture/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/pinned-tabs/",
            f"{settings.FXC_BASE_URL}/en-US/features/pinned-tabs/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/private-browsing/",
            f"{settings.FXC_BASE_URL}/en-US/features/private-browsing/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/private/",
            f"{settings.FXC_BASE_URL}/en-US/features/private/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/sync/",
            f"{settings.FXC_BASE_URL}/en-US/features/sync/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/tips/",
            f"{settings.FXC_BASE_URL}/en-US/features/tips/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/features/translate/",
            f"{settings.FXC_BASE_URL}/en-US/features/translate/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/ios/testflight/",
            f"{settings.FXC_BASE_URL}/en-US/channel/ios/testflight/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/linux/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/desktop/linux/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/mac/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/desktop/mac/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/more/",
            f"{settings.FXC_BASE_URL}/en-US/more/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/set-as-default/",
            f"{settings.FXC_BASE_URL}/en-US/landing/set-as-default/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/set-as-default/thanks/",
            f"{settings.FXC_BASE_URL}/en-US/landing/set-as-default/thanks/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/unsupported-systems/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/unsupported-systems/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/en-US/firefox/windows/",
            f"{settings.FXC_BASE_URL}/en-US/browsers/desktop/windows/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/de/firefox/windows/",
            f"{settings.FXC_BASE_URL}/de/browsers/desktop/windows/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/fr-CA/firefox/windows/",
            f"{settings.FXC_BASE_URL}/fr-CA/browsers/desktop/windows/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        # Also test some without the
        (
            "/firefox/new/",
            f"{settings.FXC_BASE_URL}/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/firefox/set-as-default/",
            f"{settings.FXC_BASE_URL}/landing/set-as-default/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
        (
            "/firefox/browsers/incognito-browser/",
            f"{settings.FXC_BASE_URL}/more/incognito-browser/{EXPECTED_REDIRECT_QS}",
            301,
            False,
        ),
    ],
)
def test_springfield_redirect_patterns(
    client,
    path,
    expected_location,
    expected_status,
    follow_redirects,
):
    response = client.get(
        path,
        follow=follow_redirects,
    )
    assert response.status_code == expected_status
    if expected_status in [200, 404]:
        assert "Location" not in response.headers
    else:
        assert response.headers["Location"] == expected_location


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,expected_location,expected_status,follow_redirects",
    [
        (
            "/en-US/firefox/installer-help/?channel=beta&installer_lang=en_US",
            f"{settings.FXC_BASE_URL}/en-US/download/installer-help/?redirect_source=mozilla-org&channel=beta&installer_lang=en_US",
            301,
            False,
        ),
        (
            "/en-US/firefox/new/?foo=bar",
            f"{settings.FXC_BASE_URL}/en-US/?redirect_source=mozilla-org&foo=bar",
            301,
            False,
        ),
    ],
)
def test_springfield_redirects_carry_over_querystrings_and_add_redirect_source(
    client,
    path,
    expected_location,
    expected_status,
    follow_redirects,
):
    response = client.get(
        path,
        follow=follow_redirects,
    )
    assert response.status_code == expected_status
    if expected_status in [200, 404]:
        assert "Location" not in response.headers
    else:
        assert response.headers["Location"] == expected_location


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    (
        "/en-US/firefox/landing/get/",
        "/en-US/firefox/138.0/whatsnew/",
        "/en-US/firefox/nightly/firstrun/",
        "/en-US/firefox/welcome/19/",
        "/en-US/firefox/download/thanks/",
    ),
)
def test_paths_not_to_be_redirected_to_springfield(client, path):
    resp = client.get(path, follow=False)
    assert "Location" not in resp.headers
    assert resp.status_code == 200


def test_mobile_app_redirector_does_not_go_to_springfield(client):
    resp = client.get("/en-US/firefox/browsers/mobile/app/")
    assert resp.status_code == 301
    assert resp.headers["Location"] == "https://apps.apple.com/app/apple-store/id989804926"


def test_mobile_app_redirector_via_adjust_firefox_android_with_campaign():
    rf = RequestFactory()
    req = rf.get("/firefox/app/?via=adjust&campaign=firefox-all", HTTP_USER_AGENT=ANDROID_UA)
    result = mobile_app_redirector(req, "firefox", "firefox-all")
    assert result == f"{settings.ADJUST_FIREFOX_ANDROID_LINK}&campaign=firefox-all"


def test_mobile_app_redirector_via_adjust_firefox_android_no_campaign():
    rf = RequestFactory()
    req = rf.get("/firefox/app/?via=adjust", HTTP_USER_AGENT=ANDROID_UA)
    assert mobile_app_redirector(req, "firefox", None) == settings.ADJUST_FIREFOX_ANDROID_LINK


def test_mobile_app_redirector_via_adjust_ignored_for_focus_android():
    rf = RequestFactory()
    req = rf.get("/firefox/app/?via=adjust&campaign=firefox-all", HTTP_USER_AGENT=ANDROID_UA)
    result = mobile_app_redirector(req, "focus", "firefox-all")
    assert result.startswith(settings.GOOGLE_PLAY_FOCUS_LINK)
    assert "utm_campaign%3Dfirefox-all" in result
    assert "app.adjust.com" not in result


def test_mobile_app_redirector_via_adjust_ignored_for_firefox_ios():
    rf = RequestFactory()
    req = rf.get("/firefox/app/?via=adjust&campaign=firefox-all", HTTP_USER_AGENT=IOS_UA)
    result = mobile_app_redirector(req, "firefox", "firefox-all")
    assert result.startswith("https://apps.apple.com/app/apple-store/id989804926")
    assert "ct=firefox-all" in result
    assert "app.adjust.com" not in result


def test_mobile_app_redirector_unknown_via_value_falls_back_to_default():
    rf = RequestFactory()
    req = rf.get("/firefox/app/?via=bogus&campaign=firefox-all", HTTP_USER_AGENT=ANDROID_UA)
    result = mobile_app_redirector(req, "firefox", "firefox-all")
    assert result.startswith(settings.GOOGLE_PLAY_FIREFOX_LINK)
    assert "utm_campaign%3Dfirefox-all" in result
    assert "app.adjust.com" not in result


def test_mobile_app_redirector_no_via_param_falls_back_to_default():
    rf = RequestFactory()
    req = rf.get("/firefox/app/?campaign=firefox-all", HTTP_USER_AGENT=ANDROID_UA)
    result = mobile_app_redirector(req, "firefox", "firefox-all")
    assert result.startswith(settings.GOOGLE_PLAY_FIREFOX_LINK)
    assert "utm_campaign%3Dfirefox-all" in result
    assert "app.adjust.com" not in result


@pytest.mark.parametrize(
    "path, expected_dest",
    (
        ("/en-US/firefox/new/?hello=world", f"{settings.FXC_BASE_URL}/en-US/{EXPECTED_REDIRECT_QS}&hello=world"),
        ("/en-US/firefox/new/", f"{settings.FXC_BASE_URL}/en-US/{EXPECTED_REDIRECT_QS}"),
        (
            "/en-US/firefox/installer-help/?bar=baz&bam=bam",
            f"{settings.FXC_BASE_URL}/en-US/download/installer-help/{EXPECTED_REDIRECT_QS}&bar=baz&bam=bam",
        ),
        ("/en-US/firefox/installer-help/", f"{settings.FXC_BASE_URL}/en-US/download/installer-help/{EXPECTED_REDIRECT_QS}"),
    ),
)
def test_subsequent_redirects_do_not_carry_querystrings_from_earlier_requests(
    client,
    path,
    expected_dest,
):
    # Safety check that Django/Bedrock isn't cacheing querystrings used in other
    # responses. Both of the paramatrized paths above have been used in earlier
    # tests in this suite, where they DID include extra querystrings, which should
    # NOT appear in the responses for this test. We also include dupes here
    resp = client.get(path, secure=True)
    assert resp.status_code == 301
    assert resp.headers["Location"] == expected_dest


@pytest.mark.parametrize(
    "path, expected_dest",
    (
        ("/firefox/new/", f"{settings.FXC_BASE_URL}/{EXPECTED_REDIRECT_QS}"),
        ("/firefox/set-as-default/", f"{settings.FXC_BASE_URL}/landing/set-as-default/{EXPECTED_REDIRECT_QS}"),
        ("/firefox/browsers/incognito-browser/", f"{settings.FXC_BASE_URL}/more/incognito-browser/{EXPECTED_REDIRECT_QS}"),
    ),
)
def test_offsite_redirects_still_work_when_locale_not_in_source_path(
    client,
    path,
    expected_dest,
):
    # Our redirects kick in before our locale-prepending middleware, so we may
    # find we have some redirects that don't have a locale when they send the
    # user to www.firefox.com
    resp = client.get(path, secure=True)
    assert resp.status_code == 301
    assert resp.headers["Location"] == expected_dest


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path, expected",
    (
        (
            "/en-US/firefox/notes/",
            "/en-US/firefox/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/notes/?foo=bar",
            "/en-US/firefox/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/android/notes/",
            "/en-US/firefox/android/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/android/notes/?foo=bar",
            "/en-US/firefox/android/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/ios/notes/",
            "/en-US/firefox/ios/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/ios/notes/?foo=bar",
            "/en-US/firefox/ios/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/aurora/notes/",
            "/en-US/firefox/aurora/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/aurora/notes/?foo=bar",
            "/en-US/firefox/aurora/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/beta/notes/",
            "/en-US/firefox/beta/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/beta/notes/?foo=bar",
            "/en-US/firefox/beta/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/developer/notes/",
            "/en-US/firefox/developer/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/developer/notes/?foo=bar",
            "/en-US/firefox/developer/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/nightly/notes/",
            "/en-US/firefox/nightly/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/nightly/notes/?foo=bar",
            "/en-US/firefox/nightly/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/organizations/notes/",
            "/en-US/firefox/organizations/notes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/organizations/notes/?foo=bar",
            "/en-US/firefox/organizations/notes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/140.0/releasenotes/",
            "/en-US/firefox/140.0/releasenotes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/140.0/releasenotes/?foo=bar",
            "/en-US/firefox/140.0/releasenotes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/android/140.0/releasenotes/",
            "/en-US/firefox/android/140.0/releasenotes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/ios/140.0/releasenotes/?foo=bar",
            "/en-US/firefox/ios/140.0/releasenotes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/releasenotes/",
            "/en-US/firefox/releasenotes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/releasenotes/?foo=bar",
            "/en-US/firefox/releasenotes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/latest/releasenotes/",
            "/en-US/firefox/latest/releasenotes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/latest/releasenotes/?foo=bar",
            "/en-US/firefox/latest/releasenotes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/android/releasenotes/",
            "/en-US/firefox/android/releasenotes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/android/releasenotes/?foo=bar",
            "/en-US/firefox/android/releasenotes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/ios/releasenotes/",
            "/en-US/firefox/ios/releasenotes/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/ios/releasenotes/?foo=bar",
            "/en-US/firefox/ios/releasenotes/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/nightly/notes/feed/",
            "/en-US/firefox/nightly/notes/feed/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/nightly/notes/feed/?foo=bar",
            "/en-US/firefox/nightly/notes/feed/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/system-requirements/",
            "/en-US/firefox/system-requirements/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/system-requirements/?foo=bar",
            "/en-US/firefox/system-requirements/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/android/system-requirements/",
            "/en-US/firefox/android/system-requirements/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/android/system-requirements/?foo=bar",
            "/en-US/firefox/android/system-requirements/?redirect_source=mozilla-org&foo=bar",
        ),
        (
            "/en-US/firefox/ios/system-requirements/",
            "/en-US/firefox/ios/system-requirements/?redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/ios/system-requirements/?foo=bar",
            "/en-US/firefox/ios/system-requirements/?redirect_source=mozilla-org&foo=bar",
        ),
    ),
)
def test_releasenotes_and_sysreq_redirects(client, path, expected):
    resp = client.get(path)
    assert resp.status_code == 301
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}{expected}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "source_path, dest_path",
    (
        (
            "/en-US/firefox/system-requirements/",
            "/en-US/firefox/system-requirements/",
        ),
        (
            "/en-US/firefox/releases/",
            "/releases/",
        ),
    ),
)
def test_releasenotes_and_sysreq_generic_urls_are_redirected_to_springfield(client, source_path, dest_path):
    resp = client.get(source_path)
    assert resp.status_code == 301
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}{dest_path}?redirect_source=mozilla-org"


@pytest.mark.parametrize(
    "path, expected",
    (
        # release notes / system requirements redirect to the same path on www.firefox.com
        ("/en-US/firefox/notes/", "/en-US/firefox/notes/"),
        ("/en-US/firefox/beta/notes/", "/en-US/firefox/beta/notes/"),
        ("/en-US/firefox/android/notes/", "/en-US/firefox/android/notes/"),
        ("/en-US/firefox/system-requirements/", "/en-US/firefox/system-requirements/"),
        ("/en-US/firefox/organizations/system-requirements/", "/en-US/firefox/organizations/system-requirements/"),
        # the releases index is served at /releases/ on www.firefox.com, not /firefox/releases/
        ("/en-US/firefox/releases/", "/releases/"),
        # the incoming query string is preserved
        ("/en-US/firefox/notes/?foo=bar&baz=1", "/en-US/firefox/notes/?foo=bar&baz=1"),
        ("/en-US/firefox/releases/?utm=x", "/releases/?utm=x"),
    ),
)
def test_releasenotes_redirect_view(path, expected):
    """`releasenotes_redirect` is normally shadowed by RedirectsMiddleware, so call it
    directly via RequestFactory to confirm its standalone fallback behaviour."""
    resp = releasenotes_redirect(RequestFactory().get(path))
    assert resp.status_code == 301
    assert resp["Location"] == f"{settings.FXC_BASE_URL}{expected}"


@pytest.mark.parametrize(
    "path, expected",
    (
        # path transformations defined in redirect patterns are applied correctly
        ("/en-US/firefox/features/", "/en-US/features/?redirect_source=mozilla-org"),
        ("/en-US/firefox/channel/desktop/", "/en-US/channel/desktop/?redirect_source=mozilla-org"),
        ("/en-US/firefox/enterprise/", "/en-US/browsers/enterprise/?redirect_source=mozilla-org"),
    ),
)
def test_fxc_redirect_view_delegates_to_resolver(path, expected):
    """`fxc_redirect` delegates to the redirects resolver so path transformations
    (e.g. /firefox/features/ → /features/) are applied correctly if the view is
    reached directly instead of being intercepted by RedirectsMiddleware."""
    resp = fxc_redirect(RequestFactory().get(path))
    assert resp.status_code == 301
    assert resp["Location"] == f"{settings.FXC_BASE_URL}{expected}"


@pytest.mark.parametrize(
    "path, query, expected",
    (
        (
            "/en-US/firefox/unknown/",
            {"foo": "bar"},
            "/en-US/firefox/unknown/?foo=bar&redirect_source=mozilla-org",
        ),
        (
            "/en-US/firefox/unknown/",
            {},
            "/en-US/firefox/unknown/?redirect_source=mozilla-org",
        ),
    ),
)
def test_fxc_redirect_view_fallback_preserves_full_path(path, query, expected):
    """When no redirect pattern matches, `fxc_redirect` falls back to
    FXC_BASE_URL + full path with redirect_source=mozilla-org appended."""
    with patch("bedrock.firefox.views.get_redirects_resolver") as mock_get_resolver:
        from django.urls import Resolver404

        mock_get_resolver.return_value.resolve.side_effect = Resolver404
        resp = fxc_redirect(RequestFactory().get(path, query))
    assert resp.status_code == 301
    assert resp["Location"] == f"{settings.FXC_BASE_URL}{expected}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "source_path, expected_status_code, dest_path",
    (
        (
            "/de/firefox/145.0/whatsnew/",
            301,
            "/de/whatsnew/145/",
        ),
        (
            "/en-CA/firefox/145.0/whatsnew/",
            301,
            "/en-CA/whatsnew/145/",
        ),
        (
            "/en-GB/firefox/145.0/whatsnew/",
            301,
            "/en-GB/whatsnew/145/",
        ),
        (
            "/en-US/firefox/145.0/whatsnew/",
            301,
            "/en-US/whatsnew/145/",
        ),
        (
            "/fr/firefox/145.0/whatsnew/",
            301,
            "/fr/whatsnew/145/",
        ),
        (
            "/en-US/firefox/146.0/whatsnew/",
            301,
            "/en-US/whatsnew/146/",
        ),
        (
            "/en-US/firefox/145.0.1/whatsnew/",
            301,
            "/en-US/whatsnew/145/",
        ),
        (
            "/en-US/firefox/145.0.1.2/whatsnew/",
            301,
            "/en-US/whatsnew/145/",
        ),
        (
            "/en-US/firefox/145.1.2/whatsnew/",
            301,
            "/en-US/whatsnew/145/",
        ),
        (
            "/en-US/firefox/154.1.2/whatsnew/",
            301,
            "/en-US/whatsnew/154/",
        ),
        (
            "/en-US/firefox/145.0/whatsnew/?query=string.here",
            301,
            "/en-US/whatsnew/145/?query=string.here",
        ),
        (
            "/en-US/firefox/145.0/whatsnew/?query=string.here&with=extra",
            301,
            "/en-US/whatsnew/145/?query=string.here&with=extra",
        ),
        (
            # Confirm non-default locale with region code and patch version number redirects
            "/es-ES/firefox/145.0.1.2/whatsnew/",
            301,
            "/es-ES/whatsnew/145/",
        ),
        (
            # Confirm locale with without region code and patch version number redirects
            "/uk/firefox/145.0.1.2/whatsnew/",
            301,
            "/uk/whatsnew/145/",
        ),
        # Routes NOT matching the redirect
        # Nightly, Beta/Developer and ESR should not redirect
        ("/en-US/firefox/145.0a/whatsnew/", 200, None),
        ("/en-US/firefox/146.0b/whatsnew/", 200, None),
        ("/en-US/firefox/146.0beta/whatsnew/", 200, None),
        ("/en-US/firefox/145.0.1a/whatsnew/", 200, None),
        ("/en-US/firefox/145.1.2b/whatsnew/", 200, None),
        ("/en-US/firefox/145.0esr/whatsnew/", 200, None),
        # And lower than 145 is not redirected
        ("/en-US/firefox/144.0/whatsnew/", 200, None),
        ("/en-US/firefox/143.0/whatsnew/", 200, None),
        ("/en-US/firefox/142.0.1/whatsnew/", 200, None),
    ),
)
def test_wnp145_redirects_to_fxc_when_appropriate(client, source_path, expected_status_code, dest_path):
    resp = client.get(source_path)
    assert resp.status_code == expected_status_code
    if expected_status_code == 301:
        assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}{dest_path}"
    else:
        assert "Location" not in resp.headers


# --------------------------------------------------------------------------
# Issue 16367 revision - deep /firefox/all/* paths redirect once to the same
# steps under /download/all/ on www.firefox.com.
#
# Vocabularies and combination rules are shared with the legacy view
# (FIREFOX_ALL_* + check_firefox_all_combination in bedrock.firefox.views):
# nothing here is re-enumerated by hand. settings.LANGUAGES drives the page
# locale alternation - the same canonical list the locale middleware
# normalizes against - so non-canonical spellings (en-us, de-AT, xx-XX) keep
# their pre-existing locale-middleware handling instead of redirecting here.
# Fragments never reach a server and are therefore excluded everywhere.
# --------------------------------------------------------------------------


PRODUCT_SLUGS = list(FIREFOX_ALL_PRODUCTS)
PLATFORM_SLUGS = list(FIREFOX_ALL_PLATFORM_MAP)
SUPPORTED_PAGE_LOCALES = [lang for lang, name in settings.LANGUAGES]


@pytest.fixture
def reprime_product_details_cache():
    """Re-prime the shared product-details cache before the test.

    Other test modules clear this cache and prime it with FirefoxDesktop
    instances whose storage layout differs from the default product_details
    storage (pre-existing cross-test pollution). #16367 tests that read
    channel/build data through the view's own data path request this fixture
    so every read re-reads from the default storage, matching production.
    Tests that never touch product-details data must not request it.
    """
    from django.core.cache import caches

    caches["product-details"].clear()
    yield


def get_redirect_response(client, path):
    """GET a path and require the first response to be the final 301 (one hop)."""
    resp = client.get(path, secure=True)
    assert resp.status_code == 301
    return resp


def assert_not_redirected_to_fxc(client, path):
    """Assert the original local handling: 404, no offsite Location."""
    resp = client.get(path, secure=True)
    assert resp.status_code == 404, (path, resp.status_code)
    assert "Location" not in resp.headers


def call_firefox_all_view(product_slug=None, platform=None, locale=None, page_locale="en-US"):
    """Call the real firefox_all view directly (the handler the request reaches
    when RedirectsMiddleware declines). Raises Http404 exactly as before."""
    request = RequestFactory().get(f"/en-US/firefox/all/{product_slug or ''}/{platform or ''}/{locale or ''}", secure=True)
    request.locale = page_locale
    return firefox_all(request, product_slug=product_slug, platform=platform, locale=locale)


# ---------------------------------------------------------------------------
# Root rules (predating this issue) must be byte-for-byte unchanged.
# ---------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize(
    "source_path,dest_path",
    (
        ("/en-US/firefox/all/", "/en-US/download/all/"),
        ("/fr/firefox/all/", "/fr/download/all/"),
        ("/sco/firefox/all/", "/sco/download/all/"),
    ),
)
def test_firefox_all_root_redirects_are_unchanged(client, source_path, dest_path):
    resp = get_redirect_response(client, source_path)
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}{dest_path}{EXPECTED_REDIRECT_QS}"


# ---------------------------------------------------------------------------
# Product-only step: every legal product (dynamic, from the shared definition).
# ---------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("product", PRODUCT_SLUGS)
def test_firefox_all_product_step_redirects(client, product):
    resp = get_redirect_response(client, f"/en-US/firefox/all/{product}/")
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}/en-US/download/all/{product}/{EXPECTED_REDIRECT_QS}"


# ---------------------------------------------------------------------------
# Platform step: representative (product, platform) combinations spanning every
# product family and each special platform rule - the redirect decision must
# agree with the real view's own decision (drift oracle). The full legal matrix
# was verified exhaustively during the audit and the registry is asserted to be
# built from the shared vocabularies (see the ordering test below).
# ---------------------------------------------------------------------------
PLATFORM_STEP_SAMPLES = (
    ("desktop-release", "win64"),
    ("desktop-release", "win-store"),  # allowed for release
    ("desktop-release", "osx"),
    ("desktop-beta", "win-store"),  # allowed for beta
    ("desktop-esr", "linux"),
    ("desktop-esr", "linux64-aarch64"),
    ("desktop-nightly", "win64"),
    ("desktop-developer", "osx"),
    ("android-release", "win64"),  # mobile quirk: segment validated then overridden
    ("mobile-release", "win64"),
    ("android-beta", "osx"),
    ("ios-release", "win64"),
    ("ios-beta", "osx"),
    ("mobile-release", "bogus-platform"),  # invalid -> 404
    ("desktop-esr", "bogus-platform"),  # invalid -> 404
    ("bogus-product", "win64"),  # invalid -> 404
)


@pytest.mark.django_db
@pytest.mark.parametrize("product,platform", PLATFORM_STEP_SAMPLES)
def test_firefox_all_platform_step_matches_the_view(reprime_product_details_cache, client, product, platform):
    try:
        call_firefox_all_view(product_slug=product, platform=platform)
        view_renders = True
    except Http404:
        view_renders = False

    resp = client.get(f"/en-US/firefox/all/{product}/{platform}/", secure=True)
    if view_renders:
        assert resp.status_code == 301
        assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}/en-US/download/all/{product}/{platform}/{EXPECTED_REDIRECT_QS}"
    else:
        assert resp.status_code == 404
        assert "Location" not in resp.headers


# ---------------------------------------------------------------------------
# Download-locale acceptance agrees with the view's own decision for a
# representative slice of product_details.languages: canonical spells, hyphen
# and special shapes, case errors, and nightly-only locales without a build.
# All 169 slugs were verified exhaustively against the view during the audit.
# ---------------------------------------------------------------------------
DOWNLOAD_LOCALE_SAMPLES = (
    "en-US",  # plain canonical
    "de",  # short canonical
    "ja",  # short canonical
    "zh-CN",  # region canonical
    "hi-IN",
    "ca-valencia",  # word-suffix canonical
    "skr",  # three-letter canonical
    "sco",
    # in product_details.languages but without a build on the release channel
    "bo",  # nightly-only locale
    "meh",  # nightly-only locale
    "sat",  # non-canonical slug
    "ckb",
    "scn",
    "wo",
    "x-testing",
    "ja-JP-mac",  # mac-suffixed slug
    "ltg",
    "brx",
    "bogus-locale",  # not in product_details at all
)


@pytest.mark.django_db
@pytest.mark.parametrize("download_locale", DOWNLOAD_LOCALE_SAMPLES)
def test_download_locale_acceptance_matches_the_view(reprime_product_details_cache, client, download_locale):
    try:
        call_firefox_all_view(product_slug="desktop-release", platform="win64", locale=download_locale)
        view_renders = True
    except Http404:
        view_renders = False

    resp = client.get(f"/en-US/firefox/all/desktop-release/win64/{download_locale}/", secure=True)
    if view_renders:
        assert resp.status_code == 301
        assert (
            resp.headers["Location"] == f"{settings.FXC_BASE_URL}/en-US/download/all/desktop-release/win64/{download_locale}/{EXPECTED_REDIRECT_QS}"
        )
    else:
        assert resp.status_code == 404
        assert "Location" not in resp.headers


# Channel-aware build validation: nightly-only locales 404 on other channels
# and redirect on nightly (channel availability comes from the view's data).
@pytest.mark.django_db
@pytest.mark.parametrize(
    "product,lang,expected",
    (
        ("desktop-developer", "bo", 404),  # nightly-only locale
        ("desktop-nightly", "meh", 301),  # exists on nightly
        ("desktop-release", "bo", 404),  # nightly-only locale
    ),
)
def test_firefox_all_channel_build_availability(reprime_product_details_cache, client, product, lang, expected):
    if expected == 301:
        resp = get_redirect_response(client, f"/en-US/firefox/all/{product}/win64/{lang}/")
        assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}/en-US/download/all/{product}/win64/{lang}/{EXPECTED_REDIRECT_QS}"
    else:
        assert_not_redirected_to_fxc(client, f"/en-US/firefox/all/{product}/win64/{lang}/")


# Download steps for page locales that differ from the download locale.
@pytest.mark.django_db
@pytest.mark.parametrize(
    "source_path,dest_path",
    (
        ("/en-US/firefox/all/desktop-release/win64/en-US/", "/en-US/download/all/desktop-release/win64/en-US/"),
        ("/fr/firefox/all/desktop-release/win64/fr/", "/fr/download/all/desktop-release/win64/fr/"),
        ("/de/firefox/all/desktop-esr/osx/de/", "/de/download/all/desktop-esr/osx/de/"),
        ("/ja/firefox/all/desktop-nightly/win64/ja/", "/ja/download/all/desktop-nightly/win64/ja/"),
        ("/en-US/firefox/all/desktop-esr/osx/sco/", "/en-US/download/all/desktop-esr/osx/sco/"),
        ("/fr/firefox/all/desktop-release/win64/en-US/", "/fr/download/all/desktop-release/win64/en-US/"),
        ("/hi-IN/firefox/all/desktop-release/win64-msi/hi-IN/", "/hi-IN/download/all/desktop-release/win64-msi/hi-IN/"),
        ("/zh-CN/firefox/all/desktop-release/win64-aarch64/zh-CN/", "/zh-CN/download/all/desktop-release/win64-aarch64/zh-CN/"),
        ("/ca/firefox/all/desktop-release/win/ca-valencia/", "/ca/download/all/desktop-release/win/ca-valencia/"),
        # win-store download step (valid for desktop-release/desktop-beta)
        ("/en-US/firefox/all/desktop-release/win-store/de/", "/en-US/download/all/desktop-release/win-store/de/"),
        ("/en-US/firefox/all/desktop-beta/win-store/en-US/", "/en-US/download/all/desktop-beta/win-store/en-US/"),
    ),
)
def test_firefox_all_download_step_redirects(reprime_product_details_cache, client, source_path, dest_path):
    resp = get_redirect_response(client, source_path)
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}{dest_path}{EXPECTED_REDIRECT_QS}"


# ---------------------------------------------------------------------------
# win-store: legal for desktop-release/desktop-beta at BOTH depths (platform
# and download), illegal for every other product at both depths.
# ---------------------------------------------------------------------------
WIN_STORE_SAMPLES = (
    "desktop-release",  # allowed
    "desktop-beta",  # allowed
    "desktop-esr",  # forbidden representative
    "mobile-release",  # forbidden mobile representative
)


@pytest.mark.django_db
@pytest.mark.parametrize("product", WIN_STORE_SAMPLES)
@pytest.mark.parametrize("depth_kwargs", ({"platform": "win-store"}, {"platform": "win-store", "locale": "en-US"}))
def test_firefox_all_win_store_combinations_match_the_view(reprime_product_details_cache, client, product, depth_kwargs):
    try:
        call_firefox_all_view(product_slug=product, **depth_kwargs)
        view_renders = True
    except Http404:
        view_renders = False

    path = "/en-US/firefox/all/{}/{}/".format(product, "/".join(v for v in depth_kwargs.values()))
    resp = client.get(path, secure=True)
    if view_renders:
        assert resp.status_code == 301
        assert (
            resp.headers["Location"]
            == f"{settings.FXC_BASE_URL}/en-US/download/all/{product}/" + "/".join(depth_kwargs.values()) + f"/{EXPECTED_REDIRECT_QS}"
        )
    else:
        assert resp.status_code == 404
        assert "Location" not in resp.headers


# Other Windows platforms are never blocked by the win-store rule.
@pytest.mark.django_db
@pytest.mark.parametrize("platform", [p for p in PLATFORM_SLUGS if p != "win-store"])
def test_firefox_all_other_windows_platforms_still_redirect(client, platform):
    resp = get_redirect_response(client, f"/en-US/firefox/all/desktop-esr/{platform}/")
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}/en-US/download/all/desktop-esr/{platform}/{EXPECTED_REDIRECT_QS}"


# ---------------------------------------------------------------------------
# Page locales: canonical spellings are forwarded (same policy as the existing
# root rule, live-verified on main); non-canonical spellings keep the locale
# middleware's normalization hop.
# ---------------------------------------------------------------------------
PAGE_LOCALE_SAMPLES = ("en-US", "en-CA", "fr", "de", "ja", "sco", "skr", "hi-IN", "zh-CN", "ca")


@pytest.mark.django_db
@pytest.mark.parametrize("page_locale", PAGE_LOCALE_SAMPLES)
def test_supported_page_locales_are_forwarded(client, page_locale):
    resp = get_redirect_response(client, f"/{page_locale}/firefox/all/desktop-esr/")
    assert resp.headers["Location"] == f"{settings.FXC_BASE_URL}/{page_locale}/download/all/desktop-esr/{EXPECTED_REDIRECT_QS}"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,expected_status,expected_location",
    (
        # lowercase: the locale middleware keeps its case-normalization hop
        ("/en-us/firefox/all/desktop-esr/", 302, "/en-US/firefox/all/desktop-esr/"),
        # fully unknown: no redirect from the step rules
        ("/xx-XX/firefox/all/desktop-esr/", 302, "/en-US/xx-XX/firefox/all/desktop-esr/"),
        # unknown region: kept as a region-strip hop
        ("/de-AT/firefox/all/desktop-esr/", 302, "/de/firefox/all/desktop-esr/"),
    ),
)
def test_non_canonical_page_locales_keep_locale_middleware_handling(client, path, expected_status, expected_location):
    resp = client.get(path, secure=True)
    assert resp.status_code == expected_status
    assert resp.headers.get("Location") == expected_location


# ---------------------------------------------------------------------------
# Query-string semantics (parsed-param comparison; fragments are client-side
# only and never reach the server).
# ---------------------------------------------------------------------------
QUERY_CASES = (
    ("", {"redirect_source": ["mozilla-org"]}),
    ("x=1", {"redirect_source": ["mozilla-org"], "x": ["1"]}),
    ("x=1&y=2", {"redirect_source": ["mozilla-org"], "x": ["1"], "y": ["2"]}),
    ("x=1&x=2", {"redirect_source": ["mozilla-org"], "x": ["1", "2"]}),
    ("x=", {"redirect_source": ["mozilla-org"]}),  # blank value dropped by parse_qs; preset kept
    ("flag", {"redirect_source": ["mozilla-org"]}),  # valueless flag: parse_qs ignores it
    ("x=a%20b", {"redirect_source": ["mozilla-org"], "x": ["a b"]}),
    ("redirect_source=other", {"redirect_source": ["other"]}),
    ("redirect_source=other&redirect_source=second", {"redirect_source": ["other", "second"]}),
    ("REDIRECT_SOURCE=upper", {"redirect_source": ["mozilla-org"], "REDIRECT_SOURCE": ["upper"]}),
    ("redirect_source=mozilla-org", {"redirect_source": ["mozilla-org"]}),
    ("redirect_source=other&via=adjust", {"redirect_source": ["other"], "via": ["adjust"]}),
)


@pytest.mark.django_db
@pytest.mark.parametrize("query,expected_params", QUERY_CASES)
def test_firefox_all_querystring_semantics(client, query, expected_params):
    resp = get_redirect_response(client, f"/en-US/firefox/all/desktop-esr/osx/sco/?{query}")
    location = resp.headers["Location"]
    assert location.count("?") == 1  # no double question mark
    actual = {}
    for k, v in parse_qsl(location.split("?", 1)[1], keep_blank_values=True):
        actual.setdefault(k, []).append(v)
    assert actual == expected_params


# ---------------------------------------------------------------------------
# Invalid paths / over-matching / input safety: no path that 404s on
# origin/main may be redirected, and no injection can change the target.
# ---------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    (
        "/en-US/firefox/all/bogus-product/",
        "/en-US/firefox/all/xdesktop-esr/",
        "/en-US/firefox/all/desktop-esrx/",
        "/en-US/firefox/all/desktop-esr/bogus-platform/",
        "/en-US/firefox/all/desktop-release/xwin64/",
        "/en-US/firefox/all/desktop-release/win64x/",
        "/en-US/firefox/all/desktop-release/win64/en-US/extra/",
        "/en-US/firefox/ALL/desktop-esr/",
        "/en-US/firefox/all/desktop-release%2Fwin64/en-US/extra/",
    ),
)
def test_firefox_all_invalid_paths_are_not_redirected(client, path):
    assert_not_redirected_to_fxc(client, path)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "injection",
    (
        "//evil.example",
        "https:",
        "@evil.example",
        "%2F%2Fevil.example",
        "%5C",
        "%0d%0a",
        "..",
        "..%2F..%2F",
        "a" * 300,
        "desktop-release?x=1",
        "desktop-release#frag",
    ),
)
def test_input_injection_safety(client, injection):
    resp = client.get(f"/en-US/firefox/all/{injection}/", secure=True)
    location = resp.headers.get("Location")
    assert resp.status_code != 500, injection
    if location is None:
        return
    parsed = urlparse(location)
    if parsed.netloc:
        assert parsed.scheme == "https"
        assert parsed.netloc == urlparse(settings.FXC_BASE_URL).netloc
        assert "/download/all/" in parsed.path
    else:
        assert location.startswith("/"), (injection, location)


# Host and loop invariants for the happy paths.
@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,dest_path",
    (
        ("/en-US/firefox/all/desktop-esr/", "/en-US/download/all/desktop-esr/"),
        ("/sco/firefox/all/desktop-esr/osx/sco/", "/sco/download/all/desktop-esr/osx/sco/"),
        ("/firefox/all/desktop-release/win64/", "/download/all/desktop-release/win64/"),
        ("/en-US/firefox/all/android-release/win64/", "/en-US/download/all/android-release/win64/"),
    ),
)
def test_firefox_all_redirects_host_and_loop_safety(client, path, dest_path):
    resp = get_redirect_response(client, path)
    location = resp.headers["Location"]
    parsed = urlparse(location)
    assert parsed.scheme == "https"  # strict scheme
    assert parsed.netloc == urlparse(settings.FXC_BASE_URL).netloc  # strictly the configured host
    assert "/download/all/" in parsed.path  # allowed namespace, after the page locale
    assert "mozilla.org" not in location  # never back to this site
    assert not location.startswith("//")  # no protocol-relative URL
    assert "//" not in parsed.path  # no double slashes in the path
    assert all(ch.isprintable() for ch in location)  # no control characters


# ---------------------------------------------------------------------------
# Drift guard: the combined redirect registry must contain the three step rules
# in deepest-first order, before the trailing global catch-alls registered by
# bedrock.redirects (last INSTALLED_APPS entry).
# ---------------------------------------------------------------------------
def test_firefox_all_rules_are_ordered_before_the_catch_alls():
    import bedrock.redirects.util as redirect_util

    regexes = [p.pattern.regex.pattern for p in redirect_util.redirectpatterns if getattr(p, "pattern", None) is not None]

    def index_of(fragment, last=False):
        matches = [i for i, r in enumerate(regexes) if fragment in r]
        assert matches, f"pattern not found in registry: {fragment}"
        return matches[-1] if last else matches[0]

    root = index_of("firefox/all/$")
    deep3 = index_of("/(?P<download_locale>")
    deep2 = index_of("/(?P<platform>%s)/?$" % "|".join(PLATFORM_SLUGS))
    deep1 = index_of("firefox/all/(?P<product>%s)/?$" % "|".join(PRODUCT_SLUGS))
    catchall = index_of("^(.*)/index\\.html$", last=True)
    assert root < deep3  # existing root rule still comes first
    assert deep3 < deep2 < deep1  # deepest-first
    assert deep1 < catchall  # step rules precede the global catch-alls


# ---------------------------------------------------------------------------
# Legacy paths intentionally unchanged by this issue.
# ---------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize(
    "source_path,dest_path",
    (
        # all-older.html already goes straight to the fxc root (with page
        # locale) via a plain redirect - no redirect_source parameter.
        ("/en-US/firefox/all-older.html", f"{settings.FXC_BASE_URL}/en-US/"),
        ("/products/firefox/all", "/firefox/all/"),
        ("/products/firefox/all.html", "/firefox/all/"),
        ("/firefox/all.html", "/firefox/all/"),
        ("/firefox/all", "/firefox/all/"),
    ),
)
def test_firefox_all_legacy_paths_unchanged(client, source_path, dest_path):
    resp = client.get(source_path, secure=True)
    assert resp.status_code == 301
    assert resp.headers["Location"] == dest_path
