# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from bedrock.mozorg.util import page

urlpatterns = (
    page("", "stories/landing.html"),
    page("art-of-engagement/", "stories/articles/art-of-engagement.html"),
    page("build-together/", "stories/articles/build-together.html"),
    page("community-champion/", "stories/articles/community-champion.html"),
    page("joy-of-color/", "stories/articles/joy-of-color.html"),
)
