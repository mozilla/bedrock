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
            "/en-US/firefox/releasenotes/",
            f"https://www.firefox.com/firefox/releasenotes/{EXPECTED_REDIRECT_QS}",
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
            "/firefox/browsers/best-browser/",
            f"https://www.firefox.com/more/best-browser/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        (
            "/firefox/features/adblocker/",
            f"https://www.firefox.com/features/adblocker/{EXPECTED_REDIRECT_QS}",
            EXPECTED_FIREFOX_COM_REDIRECT_CODE,
            False,
        ),
        # ("/firefox/browsers/compare/ie/", None, 404),
        # ("/firefox/browsers/quantum/", None, 404),
    ],
)
def test_springfield_redirect_patterns(client, path, expected_location, expected_status, follow_redirects):
    response = client.get(
        path,
        follow=follow_redirects,
    )
    assert response.status_code == expected_status
    if expected_status in [200, 404]:
        assert "Location" not in response.headers
    else:
        assert response.headers["Location"] == expected_location
