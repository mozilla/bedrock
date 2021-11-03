# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from bedrock.exp import views
from bedrock.mozorg.util import page

urlpatterns = (
    page("opt-out", "exp/opt-out.html"),
    page("firefox", "exp/firefox/index.html", ftl_files=["firefox/home"]),
    url(r"^firefox/new/$", views.new, name="exp.firefox.new"),
    url(r"^$", views.home_view, name="exp.mozorg.home"),
    page("firefox/accounts", "exp/firefox/accounts.html", ftl_files=["firefox/accounts"]),
)
