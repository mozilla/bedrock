# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page

urlpatterns = (
    page("about/", "externalpages/pocket/about.html"),
    page("add/", "externalpages/pocket/add.html"),
    page("android/", "externalpages/pocket/android.html"),
    page("ios/", "externalpages/pocket/ios.html"),
    page("chrome/", "externalpages/pocket/chrome.html"),
    page("safari/", "externalpages/pocket/safari.html"),
    page("opera/", "externalpages/pocket/opera.html"),
    page("edge/", "externalpages/pocket/edge.html"),
    page("welcome/", "externalpages/pocket/welcome.html"),
    page("contact-info/", "externalpages/pocket/contact-info.html"),
    page("firefox/new_tab_learn_more/", "externalpages/pocket/firefox/new-tab-learn-more.html"),
    page("pocket-and-firefox/", "externalpages/pocket/pocket-and-firefox.html"),
    page("get-inspired/", "externalpages/pocket/get-inspired.html"),
    page("jobs/", "externalpages/pocket/jobs.html"),
    page("privacy/", "externalpages/pocket/privacy.html"),
    page("tos/", "externalpages/pocket/tos.html"),
    page("save-to-pocket/", "externalpages/pocket/save-to-pocket.html"),
)
