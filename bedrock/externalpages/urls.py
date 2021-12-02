# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page

urlpatterns = (
    page("pocket/about", "externalpages/pocket/about.html"),
    page("pocket/add", "externalpages/pocket/add.html"),
    page("pocket/android", "externalpages/pocket/android.html"),
    page("pocket/ios", "externalpages/pocket/ios.html"),
    page("pocket/chrome", "externalpages/pocket/chrome.html"),
    page("pocket/safari", "externalpages/pocket/safari.html"),
    page("pocket/opera", "externalpages/pocket/opera.html"),
    page("pocket/edge", "externalpages/pocket/edge.html"),
)
