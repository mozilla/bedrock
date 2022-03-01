# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.urls import path, re_path

from bedrock.mozorg.util import page
from bedrock.redirects.util import redirect

from . import views
from .feeds import LatestPositionsFeed

urlpatterns = [
    # Diversity and inclusion redirect
    redirect(r"^diversity/$", "diversity.2021.index", name="diversity", locale_prefix=False),
    # Main paths
    page("diversity/2021", "diversity/2021/index.html"),
    page("diversity/2021/what-we-build", "diversity/2021/what-we-build.html"),
    page("diversity/2021/beyond-our-products", "diversity/2021/beyond-products.html"),
    page("diversity/2021/who-we-are", "diversity/2021/who-we-are.html")
]
