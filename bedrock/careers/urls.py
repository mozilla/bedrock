# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.urls import path, re_path

from bedrock.mozorg.util import page

from . import views
from .feeds import LatestPositionsFeed

urlpatterns = [
    # Main paths
    path("", views.HomeView.as_view(), name="careers.home"),
    re_path(r"^position/(?P<source>[\w]+)/(?P<job_id>[\w]+)/$", views.PositionDetailView.as_view(), name="careers.position"),
    path("feed/", LatestPositionsFeed(), name="careers.feed"),
    path("listings/", views.PositionListView.as_view(), name="careers.listings"),
    path("internships/", views.InternshipsView.as_view(), name="careers.internships"),
    path("benefits/", views.BenefitsView.as_view(), name="careers.benefits"),
]


if settings.DEBUG:
    urlpatterns += [page("404", "careers/404.html", ftl_files=["404", "careers/404"])]
