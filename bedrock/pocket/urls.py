# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.mozorg.util import page

urlpatterns = (
    page("about/", "pocket/about.html"),
    page("add/", "pocket/add.html"),
    page("android/", "pocket/android.html"),
    page("ios/", "pocket/ios.html"),
    page("chrome/", "pocket/chrome.html"),
    page("safari/", "pocket/safari.html"),
    page("opera/", "pocket/opera.html"),
    page("edge/", "pocket/edge.html"),
    page("welcome/", "pocket/welcome.html"),
    page("contact-info/", "pocket/contact-info.html"),
    page("firefox/new_tab_learn_more/", "pocket/firefox/new-tab-learn-more.html"),
    page("pocket-and-firefox/", "pocket/pocket-and-firefox.html"),
    page("get-inspired/", "pocket/get-inspired.html"),
    page("jobs/", "pocket/jobs.html"),
    page("privacy/", "pocket/privacy.html"),
    page("tos/", "pocket/tos.html"),
    page("save-to-pocket/", "pocket/save-to-pocket.html"),
)
