# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page

urlpatterns = (
    page("pocket/about/", "externalpages/pocket/about.html"),
    page("pocket/add/", "externalpages/pocket/add.html"),
    page("pocket/android/", "externalpages/pocket/android.html"),
    page("pocket/ios/", "externalpages/pocket/ios.html"),
    page("pocket/chrome/", "externalpages/pocket/chrome.html"),
    page("pocket/safari/", "externalpages/pocket/safari.html"),
    page("pocket/opera/", "externalpages/pocket/opera.html"),
    page("pocket/edge/", "externalpages/pocket/edge.html"),
    page("pocket/welcome/", "externalpages/pocket/welcome.html"),
    page("pocket/contact-info/", "externalpages/pocket/contact-info.html"),
    page("pocket/firefox/new_tab_learn_more/", "externalpages/pocket/firefox/new-tab-learn-more.html"),
    page("pocket/pocket-and-firefox/", "externalpages/pocket/pocket-and-firefox.html"),
    page("pocket/get-inspired/", "externalpages/pocket/get-inspired.html"),
    page("pocket/jobs/", "externalpages/pocket/jobs.html"),
    page("pocket/privacy/", "externalpages/pocket/privacy.html"),
    page("pocket/tos/", "externalpages/pocket/tos.html"),
    page("pocket/save-to-pocket/", "externalpages/pocket/save-to-pocket.html"),
)
