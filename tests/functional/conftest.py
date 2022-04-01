# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest
import requests
from bs4 import BeautifulSoup

TIMEOUT = 60


@pytest.fixture
def capabilities(request, capabilities):
    driver = request.config.getoption("driver")
    if capabilities.get("browserName", driver).lower() == "firefox":
        capabilities["marionette"] = True
    return capabilities


@pytest.fixture
def driver_log():
    return "tests/functional/driver.log"


@pytest.fixture(scope="session")
def session_capabilities(pytestconfig, session_capabilities):
    driver = pytestconfig.getoption("driver")
    if driver == "SauceLabs":
        session_capabilities.setdefault("tags", []).append("bedrock")

        if session_capabilities.get("browserName", driver).lower() == "internet explorer":
            # Avoid default SauceLabs proxy for IE.
            session_capabilities["avoidProxy"] = True

            # Use JavaScript events instead of native
            # window events for more reliable IE testing.
            session_capabilities["se:ieOptions"] = {"nativeEvents": False}

    return session_capabilities


@pytest.fixture
def firefox(selenium):
    return selenium.capabilities.get("browserName").lower() == "firefox"


@pytest.fixture
def internet_explorer(selenium):
    return selenium.capabilities.get("browserName").lower() == "internet explorer"


@pytest.fixture(autouse=True)
def filter_capabilities(request):
    marker = None
    if request.node.get_closest_marker("skip_if_firefox") and request.getfixturevalue("firefox"):
        marker = request.node.get_closest_marker("skip_if_firefox")
    if request.node.get_closest_marker("skip_if_not_firefox") and not request.getfixturevalue("firefox"):
        marker = request.node.get_closest_marker("skip_if_not_firefox")
    if request.node.get_closest_marker("skip_if_internet_explorer") and request.getfixturevalue("internet_explorer"):
        marker = request.node.get_closest_marker("skip_if_internet_explorer")

    if marker:
        reason = marker.kwargs.get("reason") or marker.name
        pytest.skip(reason)


@pytest.fixture
def selenium(selenium):
    selenium.set_window_size(1280, 1024)  # width, height
    return selenium


@pytest.fixture
def selenium_mobile(selenium):
    selenium.set_window_size(320, 480)  # width, height
    return selenium


def pytest_generate_tests(metafunc):
    markexpr = metafunc.config.getoption("markexpr")
    if markexpr == "download":
        base_url = metafunc.config.getoption("base_url")
        if "download_path" in metafunc.fixturenames:
            soup = get_web_page(f"{base_url}/en-US/firefox/download/thanks/")
            urls = [a["href"] for a in soup.find("ul", class_="download-list").find_all("a")]
            # Bug 1266682 remove links to Play Store to avoid rate limiting in automation.
            urls = [url for url in urls if "play.google.com" not in url]
            assert urls
            metafunc.parametrize("download_path", urls)

        elif "download_path_l10n" in metafunc.fixturenames:
            soup = get_web_page(f"{base_url}/en-US/firefox/all/")
            lists = soup.find("div", class_="c-all-downloads")
            urls = [a["href"] for a in lists.find_all(attrs={"data-link-type": "download"})]
            assert urls
            metafunc.parametrize("download_path_l10n", urls)


def get_web_page(url):
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException:
        # retry
        r = requests.get(url, timeout=TIMEOUT)
    return BeautifulSoup(r.content, "html.parser")
