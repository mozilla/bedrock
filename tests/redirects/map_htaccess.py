# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from .base import flatten, url_test

URLS = flatten(
    (
        url_test(
            "/ignored/placeholder/to/allow/test/setup",
            "/until-we-rempove-pytest.mark.skip-from-the-test/",
        ),
    )
)
