# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from operator import itemgetter

import json
import os
import pytest
import requests
import subprocess
import time

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


def write_ssl_results(base_url, tmp_filename):
    print("get results")
    data = subprocess.check_output(["ssllabs-scan", "--quiet", base_url])
    with open(tmp_filename, "w") as file:
        file.write(data.decode())


def get_ssl_json_results(tmp_filename):
    with open(tmp_filename) as json_file:
        data = json.load(json_file)
    return data


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
