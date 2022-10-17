# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.util import page
from bedrock.redirects.util import redirect

urlpatterns = (
    page("", "stories/landing.html"),
    page("art-of-engagement/", "stories/articles/art-of-engagement.html"),
    page("build-together/", "stories/articles/build-together.html"),
    page("community-champion/", "stories/articles/community-champion.html"),
    # REMOVE WHEN REAL PAGE GOES LIVE
    redirect(r"^joy-of-color/?$", "https://blog.mozilla.org/en/products/firefox/firefox-news/independent-voices/", permanent=False),
)
