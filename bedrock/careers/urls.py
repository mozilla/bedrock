# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from . import views
from .feeds import LatestPositionsFeed

urlpatterns = [
    url(r"^$", views.HomeView.as_view(), name="careers.home"),
    url(r"^position/(?P<source>[\w]+)/(?P<job_id>[\w]+)/$", views.PositionDetailView.as_view(), name="careers.position"),
    url(r"^feed/$", LatestPositionsFeed(), name="careers.feed"),
    url(r"^listings/$", views.PositionListView.as_view(), name="careers.listings"),
    url(r"^internships/$", views.InternshipsView.as_view(), name="careers.internships"),
    url(r"^benefits/$", views.BenefitsView.as_view(), name="careers.benefits"),
]
