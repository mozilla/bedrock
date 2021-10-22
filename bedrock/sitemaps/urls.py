# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.urls import re_path

from bedrock.sitemaps.views import SitemapView

urlpatterns = (re_path(r"sitemap(?P<is_none>_none)?.xml", SitemapView.as_view()),)
