# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import os
import subprocess
import time
from operator import itemgetter

import pytest
import requests

# some parameters to use in later tests
supported_versions = (
    ("tlsv1", "1.0"),
    ("tlsv1_1", "1.1"),
    ("tlsv1_2", "1.2"),
)

unsupported_versions = (("tlsv1_3", "1.3"),)

ciphers = (
    ("weak_RSA_3DES_112", "TLS_RSA_WITH_3DES_EDE_CBC_SHA"),
    ("strong_ECDHE_RSA_AES_256", "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"),
)


# helper functions
def write_ssl_results(base_url, tmp_filename):
    print("get results")
    data = subprocess.check_output(["ssllabs-scan", "--quiet", base_url])
    with open(tmp_filename, "w") as file:
        file.write(data.decode())


def get_ssl_json_results(tmp_filename):
    with open(tmp_filename) as json_file:
        data = json.load(json_file)
    return data


# end helper functions


@pytest.mark.cdn
@pytest.fixture(scope="session")
def get_ssllabs_results(base_url):
    tmp_filename = "ssllabs_data.txt"
    if os.path.exists(tmp_filename):
        # check if file is fairly recent,
        file_time = os.stat(tmp_filename).st_mtime
        if time.time() - file_time < 600:
            return get_ssl_json_results(tmp_filename)

    write_ssl_results(base_url, tmp_filename)
    return get_ssl_json_results(tmp_filename)


@pytest.mark.cdn
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


@pytest.mark.cdn
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


@pytest.mark.cdn
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


@pytest.mark.cdn
@pytest.mark.nondestructive
def test_cdn_cache(base_url):
    full_url = "{}/{}{}".format(base_url, "en-US", "/firefox/new/")

    # hit the url once to make sure the cache is warm
    resp = requests.get(full_url, timeout=5)
    assert resp.status_code == 200

    # then test that caching is working
    resp = requests.get(full_url, timeout=5)
    assert "Hit" in resp.headers["x-cache"]


@pytest.mark.cdn
@pytest.mark.nondestructive
@pytest.mark.parametrize("version", supported_versions, ids=itemgetter(0))
def test_enabled_protocols(version, get_ssllabs_results):
    supported_protocols = get_ssllabs_results[0]["endpoints"][0]["details"]["protocols"]
    found = False
    for prot in supported_protocols:
        if prot["version"] == version[1]:
            found = True
    assert found


@pytest.mark.cdn
@pytest.mark.nondestructive
@pytest.mark.parametrize("version", unsupported_versions, ids=itemgetter(0))
def test_disabled_protocols(version, get_ssllabs_results):
    supported_protocols = get_ssllabs_results[0]["endpoints"][0]["details"]["protocols"]
    found = False
    for prot in supported_protocols:
        if prot["version"] == version[1]:
            found = True
    assert ~found


@pytest.mark.cdn
@pytest.mark.nondestructive
@pytest.mark.parametrize("cipher", ciphers, ids=itemgetter(0))
def test_enabled_ciphers(cipher, get_ssllabs_results):
    supported_suite = get_ssllabs_results[0]["endpoints"][0]["details"]["suites"]["list"]
    found = False
    for cipher_description in supported_suite:
        if cipher_description["name"] == cipher[1]:
            found = True
    assert found


@pytest.mark.cdn
@pytest.mark.cdnprod
@pytest.mark.nondestructive
def test_tls(get_ssllabs_results):
    """Check get_ssllabs_results to make sure that all expected clients connected without issue"""
    data = get_ssllabs_results

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
