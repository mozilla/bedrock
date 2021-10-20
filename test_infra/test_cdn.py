# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from pathlib import Path

import pytest
import requests

MLS_URL = "https://location.services.mozilla.com/v1/country" "?key=ec4d0c4b-b9ac-4d72-9197-289160930e14"
TESTS_PATH = Path(__file__).parent
TLS_DATA_PATH = TESTS_PATH.joinpath("fixtures", "tls.json")


@pytest.mark.parametrize(
    "url",
    (
        "/",
        "/firefox/",
        "/firefox/new/",
        "/about/",
    ),
)
@pytest.mark.nondestructive
def test_locale_redirect(url, base_url):
    resp = requests.get(f"{base_url}{url}", allow_redirects=False, headers={"accept-language": "de"})
    assert resp.status_code == 301
    assert "accept-language" in resp.headers["vary"].lower()
    assert resp.headers["location"].startswith("/de/")


@pytest.mark.parametrize(
    "url",
    (
        # only in s3
        "/media/contentcards/img/home-en/card_2/card_2.73be009fe44e.jpg",
        # comes from bedrock
        "/media/protocol/img/logos/mozilla/black.40d1af88c248.svg",
    ),
)
@pytest.mark.nondestructive
def test_media(url, base_url):
    """Verify that media is well cached and loaded from s3"""
    url = f"{base_url}{url}"
    resp = requests.head(url)
    assert resp.status_code == 200
    assert resp.headers["cache-control"] == "max-age=315360000, public, immutable"
    # this means it came from s3
    assert "x-amz-version-id" in resp.headers


@pytest.mark.nondestructive
def test_geo(base_url):
    """Make sure our geo results match MLS no matter where they're run"""
    cdn_url = f"{base_url}/country-code.json"
    mls_country = requests.get(MLS_URL).json()["country_code"]
    cdn_country = requests.get(cdn_url).json()["country_code"]
    assert cdn_country == mls_country


@pytest.mark.nondestructive
def test_query_params(base_url):
    """Query params should be respected in the cache and bedrock should respond appropriately

    Based on the `firefox_mobile_faq` function in `bedrock/firefox/redirects.py`.
    """
    url = f"{base_url}/mobile/faq/"
    resp = requests.head(url)
    assert resp.status_code == 301
    assert resp.headers["location"] == "https://support.mozilla.org/products/mobile"

    # with query string
    url = f"{base_url}/mobile/faq/?os=firefox-os"
    resp = requests.head(url)
    assert resp.status_code == 301
    assert resp.headers["location"] == "https://support.mozilla.org/products/firefox-os"


@pytest.mark.skipif(not TLS_DATA_PATH.exists(), reason="TLS data file missing")
@pytest.mark.nondestructive
def test_tls():
    """Check tls.json to make sure that all expected clients connected without issue

    To fetch the tls.json file run `make TEST_DOMAIN=www.mozilla.org tls-test-data`
    """
    with TLS_DATA_PATH.open() as tls_file:
        data = json.load(tls_file)

    errors = 0
    for endp in data[0]["endpoints"]:
        for sim in endp["details"]["sims"]["results"]:
            if sim["errorCode"] != 0:
                # IE 6 is expected to fail
                if sim["client"]["name"] == "IE" and sim["client"]["version"] == "6":
                    continue

                print(sim["client"])
                errors += 1

    assert errors == 0, "TLS SIMs Failures"
