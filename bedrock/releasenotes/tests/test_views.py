# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import pytest

from bedrock.releasenotes.views import show_android_sys_req


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
