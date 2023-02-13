# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import path

from bedrock.mozorg.util import page
from bedrock.stories import views

# note: preserving the individual story page urls for backwards compatibility with name-based url calls
urlpatterns = (
    path("", views.landing_page, name="stories.landing"),
    path("<slug:slug>/", views.story_page),
    page("art-of-engagement/", "stories/articles/art-of-engagement.html"),
    page("build-together/", "stories/articles/build-together.html"),
    page("community-champion/", "stories/articles/community-champion.html"),
    page("joy-of-color/", "stories/articles/joy-of-color.html"),
    page("raising-technology-eq/", "stories/articles/raising-technology-eq.html"),
    page("dreaming-then-building/", "stories/articles/dreaming-then-building.html"),
)
