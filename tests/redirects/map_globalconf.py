# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from .base import flatten, url_test

UA_ANDROID = {"User-Agent": "Mozilla/5.0 (Android 6.0.1; Mobile; rv:51.0) Gecko/51.0 Firefox/51.0"}
UA_IOS = {"User-Agent": "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3 like Mac OS X; de-de) AppleWebKit/533.17.9 (KHTML, like Gecko) Mobile/8F190"}

URLS = flatten(
    (
        url_test(
            "/ignored/placeholder/to/allow/test/setup",
            "/until-we-rempove-pytest.mark.skip-from-the-test/",
        ),
    )
)
