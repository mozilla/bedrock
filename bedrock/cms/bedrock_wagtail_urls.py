# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Custom version of wagtail_urls that wraps the wagtail_serve route
# with a decorator that does a lookahead to see if Wagtail will 404 or not
# (based on a precomputed cache of URLs in the CMS)

from django.urls import re_path

from wagtail.urls import urlpatterns as wagtail_urlpatterns
from wagtail.views import serve as wagtail_serve

from bedrock.cms.decorators import pre_check_for_cms_404

# Modify the wagtail_urlpatterns to replace `wagtail_serve` with a decorated
# version of the same view, so we can pre-empt Wagtail looking up a page
# that we know will be a 404
custom_wagtail_urls = []

for pattern in wagtail_urlpatterns:
    if hasattr(pattern.callback, "__name__") and pattern.callback.__name__ == "serve":
        custom_wagtail_urls.append(
            re_path(
                # This is a RegexPattern not a RoutePattern, which is why we use re_path not path
                pattern.pattern,
                pre_check_for_cms_404(wagtail_serve),
                name=pattern.name,
            )
        )
    else:
        custom_wagtail_urls.append(pattern)

# Note: custom_wagtail_urls is imported into the main project urls.py instead of wagtail_urls
