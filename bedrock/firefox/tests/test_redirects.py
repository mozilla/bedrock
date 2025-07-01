# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from unittest.mock import patch

from django.conf import settings
from django.test import RequestFactory, override_settings

import pytest

from bedrock.firefox.redirects import mobile_app, validate_param_value


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


EXPECTED_FIREFOX_COM_REDIRECT_CODE = 301 if settings.MAKE_FIREFOX_COM_REDIRECTS_PERMANENT else 302

EXPECTED_REDIRECT_QS = "?redirect_source=mozilla-org"


@override_settings(ENABLE_FIREFOX_COM_REDIRECTS=True)
@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,expected_location,expected_status,follow_redirects",
    [
        (
            "/en-US/firefox/",
            f"https://www.firefox.com{EXPECTED_REDIRECT_QS}",
            200,
            True,
        ),
        (
            "/en-US/firefox/new/",
            f"https://www.firefox.com{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/all/",
            f"https://www.firefox.com/download/all/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/installer-help/",
            f"https://www.firefox.com/download/installer-help/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/",
            f"https://www.firefox.com/{EXPECTED_REDIRECT_QS}",
            200,
            True,
        ),
        (
            "/en-US/firefox/browsers/best-browser/",
            f"https://www.firefox.com/more/best-browser/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/browser-history/",
            f"https://www.firefox.com/more/browser-history/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/chromebook/",
            f"https://www.firefox.com/browsers/desktop/chromebook/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/",
            f"https://www.firefox.com/compare/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/brave/",
            f"https://www.firefox.com/compare/brave/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/chrome/",
            f"https://www.firefox.com/compare/chrome/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/edge/",
            f"https://www.firefox.com/compare/edge/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/opera/",
            f"https://www.firefox.com/compare/opera/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/compare/safari/",
            f"https://www.firefox.com/compare/safari/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/incognito-browser/",
            f"https://www.firefox.com/more/incognito-browser/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/",
            f"https://www.firefox.com/browsers/mobile/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/android/",
            f"https://www.firefox.com/browsers/mobile/android/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/focus/",
            f"https://www.firefox.com/browsers/mobile/focus/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/mobile/ios/",
            f"https://www.firefox.com/browsers/mobile/ios/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/update-your-browser/",
            f"https://www.firefox.com/more/update-your-browser/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/what-is-a-browser/",
            f"https://www.firefox.com/more/what-is-a-browser/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/browsers/windows-64-bit/",
            f"https://www.firefox.com/more/windows-64-bit/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/channel/android/",
            f"https://www.firefox.com/channel/android/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/channel/desktop/",
            f"https://www.firefox.com/channel/desktop/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/channel/ios/",
            f"https://www.firefox.com/channel/ios/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/developer/",
            f"https://www.firefox.com/channel/desktop/developer/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/enterprise/",
            f"https://www.firefox.com/browsers/enterprise/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/faq/",
            f"https://www.firefox.com/more/faq/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/",
            f"https://www.firefox.com/features/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/adblocker/",
            f"https://www.firefox.com/features/adblocker/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/add-ons/",
            f"https://www.firefox.com/features/add-ons/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/block-fingerprinting/",
            f"https://www.firefox.com/features/block-fingerprinting/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/bookmarks/",
            f"https://www.firefox.com/features/bookmarks/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/customize/",
            f"https://www.firefox.com/features/customize/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/eyedropper/",
            f"https://www.firefox.com/features/eyedropper/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/fast/",
            f"https://www.firefox.com/features/fast/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/password-manager/",
            f"https://www.firefox.com/features/password-manager/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/pdf-editor/",
            f"https://www.firefox.com/features/pdf-editor/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/picture-in-picture/",
            f"https://www.firefox.com/features/picture-in-picture/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/pinned-tabs/",
            f"https://www.firefox.com/features/pinned-tabs/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/private-browsing/",
            f"https://www.firefox.com/features/private-browsing/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/private/",
            f"https://www.firefox.com/features/private/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/sync/",
            f"https://www.firefox.com/features/sync/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/tips/",
            f"https://www.firefox.com/features/tips/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/features/translate/",
            f"https://www.firefox.com/features/translate/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/ios/testflight/",
            f"https://www.firefox.com/channel/ios/testflight/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/linux/",
            f"https://www.firefox.com/browsers/desktop/linux/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/mac/",
            f"https://www.firefox.com/browsers/desktop/mac/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/more/",
            f"https://www.firefox.com/more/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/set-as-default/",
            f"https://www.firefox.com/landing/set-as-default/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/set-as-default/thanks/",
            f"https://www.firefox.com/landing/set-as-default/thanks/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/unsupported-systems/",
            f"https://www.firefox.com/browsers/unsupported-systems/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/windows/",
            f"https://www.firefox.com/browsers/desktop/windows/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
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


@override_settings(ENABLE_FIREFOX_COM_REDIRECTS=True)
@pytest.mark.django_db
@pytest.mark.parametrize(
    "path,expected_location,expected_status,follow_redirects",
    [
        (
            "/en-US/firefox/installer-help/?channel=beta&installer_lang=en_US",
            "https://www.firefox.com/download/installer-help/?redirect_source=mozilla-org&channel=beta&installer_lang=en_US",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/en-US/firefox/new/?foo=bar",
            "https://www.firefox.com?redirect_source=mozilla-org&foo=bar",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
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


@override_settings(ENABLE_FIREFOX_COM_REDIRECTS=True)
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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path",
    (
        "/firefox/releasenotes/",
        "/firefox/system-requirements/",
        "/firefox/android/releasenotes/",
        "/firefox/android/system-requirements/",
        "/firefox/ios/releasenotes/",
        "/firefox/ios/system-requirements/",
        "/firefox/releases/",
    ),
)
def test_releasenotes_generic_urls_not_rediected_to_springfield(client, path):
    resp = client.get(path)
    assert resp.status_code == 302
    assert "https://www.firefox.com" not in resp.headers["Location"]
