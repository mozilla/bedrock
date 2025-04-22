# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

pytestmark = pytest.mark.django_db


def _test(
    url,
    client,
    follow=False,
    expected_status=200,
    expected_content=None,
):
    resp = client.get(url, follow=follow)
    assert resp.status_code == expected_status
    if expected_content is not None:
        assert expected_content in resp.text


def test_healthz(client):
    _test(
        url="/healthz/",
        client=client,
        expected_content="pong",
    )


def test_readiness(client):
    _test(
        url="/readiness/",
        client=client,
    )


def test_healthz_cron(client):
    _test(
        url="/healthz-cron/",
        client=client,
        expected_content="Time Since Last Cron Task Runs",
        expected_status=500,  # because an unsynced DB returns a 500, but with the correct HTML
    )
