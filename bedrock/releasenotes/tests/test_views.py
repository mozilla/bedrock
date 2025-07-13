# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from pathlib import Path
from unittest.mock import patch

from django.core.cache import caches
from django.test import override_settings

import pytest

from bedrock.releasenotes.models import ProductRelease
from bedrock.releasenotes.views import release_notes, releases_index, show_android_sys_req, system_requirements

RELEASES_PATH = str(Path(__file__).parent)
release_cache = caches["release-notes"]


@pytest.mark.parametrize(
    "version_string, expected",
    (
        (None, False),
        ("", False),
        ("test", False),
        ("0", False),
        ("45", False),
        ("45.0", False),
        ("45.1.1", False),
        ("45.0a1", False),
        ("45.0a2", False),
        ("46", True),
        ("46.0", True),
        ("46.1.1", True),
        ("46.0a1", True),
        ("46.0a2", True),
        ("47", True),
        ("100", True),
        ("100.0", True),
        ("100.1.1", True),
        ("100.0a1", True),
        ("100.0a2", True),
        ("102", True),
        ("102.0", True),
        ("102.1.1", True),
        ("102.0a1", True),
        ("102.0a2", True),
    ),
)
def test_show_android_sys_req(version_string, expected):
    assert show_android_sys_req(version_string) == expected


@patch("bedrock.firefox.views.l10n_utils.render")
def test_releases_index(render_mock, rf):
    """Spot checks, incl confirmation that FF100 will not cause a hiccup"""

    # Dates are from https://wiki.mozilla.org/Release_Management/Calendar but
    # these are here just for testing/dummy purposes
    mock_major_releases_val = {
        "3.6": "2010-01-21",
        "33.0": "2014-10-14",
        "33.1": "2014-11-10",
        "96.0": "2022-01-11",
        "100.0": "2022-05-03",
        "101.0": "2022-05-31",
    }
    mock_minor_releases_val = {
        "3.6.2": "2010-03-22",
        "3.6.3": "2010-04-01",
        "3.6.4": "2010-06-22",
        "3.6.6": "2010-06-26",
        "3.6.7": "2010-07-20",
        "3.6.8": "2010-07-23",
        "3.6.9": "2010-09-07",
        "3.6.10": "2010-09-15",
        "3.6.11": "2010-10-19",
        "3.6.12": "2010-10-27",
        "3.6.13": "2010-12-09",
        "3.6.14": "2011-03-01",
        "3.6.15": "2011-03-04",
        "3.6.16": "2011-03-22",
        "33.0.1": "2014-10-24",
        "33.0.2": "2014-10-28",
        "33.0.3": "2014-11-06",
        "33.1.1": "2014-11-14",
        "96.5": "2022-01-11",  # 100% fake/test
        "100.1": "2022-05-03",  # 100% fake/test
        "100.2": "2022-05-03",  # 100% fake/test
        "101.2": "2022-05-31",  # 100% fake/test
    }

    request = rf.get("/")

    with patch("bedrock.releasenotes.views.firefox_desktop") as mock_firefox_desktop:
        mock_firefox_desktop.firefox_history_major_releases = mock_major_releases_val
        mock_firefox_desktop.firefox_history_stability_releases = mock_minor_releases_val

        releases_index(request, "Firefox")

    expected_data = {
        "releases": [
            (101.0, {"major": "101.0", "minor": ["101.2"]}),
            (
                100.0,
                {
                    "major": "100.0",
                    "minor": ["100.1", "100.2"],
                },
            ),
            (
                96.0,
                {
                    "major": "96.0",
                    "minor": ["96.5"],
                },
            ),
            (
                33.1,
                {
                    "major": "33.1",
                    "minor": ["33.1.1"],
                },
            ),
            (
                33.0,
                {
                    "major": "33.0",
                    "minor": ["33.0.1", "33.0.2", "33.0.3"],
                },
            ),
            (
                3.6,
                {
                    "major": "3.6",
                    "minor": [
                        "3.6.2",
                        "3.6.3",
                        "3.6.4",
                        "3.6.6",
                        "3.6.7",
                        "3.6.8",
                        "3.6.9",
                        "3.6.10",
                        "3.6.11",
                        "3.6.12",
                        "3.6.13",
                        "3.6.14",
                        "3.6.15",
                        "3.6.16",
                    ],
                },
            ),
        ],
    }
    render_mock.assert_called_once_with(
        request,
        "firefox/releases/index.html",
        expected_data,
    )


@patch("bedrock.firefox.views.l10n_utils.render")
def test_releases_index__product_other_than_firefox(render_mock, rf):
    request = rf.get("/")
    releases_index(request, "someproduct")
    render_mock.assert_called_once_with(
        request,
        "someproduct/releases/index.html",
        {"releases": []},
    )


@patch("bedrock.firefox.templatetags.helpers.desktop_builds")
@pytest.mark.django_db
@pytest.mark.parametrize("enable_redirects", (True, False))
def test_release_notes_detail_contains_canonical_tag_pointing_to_firefox_com_if_redirects_enabled(mock_desktop_builds, rf, enable_redirects):
    # Bootstrap relnotes test data
    with override_settings(RELEASE_NOTES_PATH=RELEASES_PATH):
        ProductRelease.objects.refresh()
        release_cache.clear()

    ver = ProductRelease.objects.last().version
    assert ver == "24.5.0"  # safety check that the data hasn't moved

    request = rf.get("/en-US/firefox/24.5.0/releasenotes/")

    with override_settings(ENABLE_FIREFOX_COM_REDIRECTS=enable_redirects):
        resp = release_notes(request, version="24.5.0")
        _link_is_in_content = '<link rel="canonical" href="https://www.firefox.com/en-US/firefox/24.5.0/releasenotes/">' in str(resp.content)
        assert _link_is_in_content == enable_redirects

    release_cache.clear()


@patch("bedrock.firefox.templatetags.helpers.desktop_builds")
@pytest.mark.django_db
@pytest.mark.parametrize("enable_redirects", (True, False))
def test_system_requirements_detail_contains_canonical_tag_pointing_to_firefox_com_if_redirects_enabled(mock_desktop_builds, rf, enable_redirects):
    # Bootstrap relnotes test data
    with override_settings(RELEASE_NOTES_PATH=RELEASES_PATH):
        ProductRelease.objects.refresh()
        release_cache.clear()

    ver = ProductRelease.objects.last().version
    assert ver == "24.5.0"  # safety check that the data hasn't moved

    request = rf.get("/en-US/firefox/24.5.0/system-requirements/")

    with override_settings(ENABLE_FIREFOX_COM_REDIRECTS=enable_redirects):
        resp = system_requirements(request, version="24.5.0")
        _link_is_in_content = '<link rel="canonical" href="https://www.firefox.com/en-US/firefox/24.5.0/system-requirements/">' in str(resp.content)
        assert _link_is_in_content == enable_redirects

    release_cache.clear()


@pytest.mark.django_db
@pytest.mark.parametrize("enable_redirects", (True, False))
def test_releases_index_contains_canonical_tag_pointing_to_firefox_com_if_redirects_enabled(rf, enable_redirects):
    # Bootstrap relnotes test data
    with override_settings(RELEASE_NOTES_PATH=RELEASES_PATH):
        ProductRelease.objects.refresh()
        release_cache.clear()

    request = rf.get("/en-US/firefox/releases/")

    with override_settings(ENABLE_FIREFOX_COM_REDIRECTS=enable_redirects):
        resp = releases_index(request, product="Firefox")
        _link_is_in_content = '<link rel="canonical" href="https://www.firefox.com/en-US/releases/">' in str(resp.content)
        assert _link_is_in_content == enable_redirects

    release_cache.clear()
