# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This module contains named URL paths which only exist in the CMS.
#
# They are named so that they can be looked up via our url() jinja
# helper, even though the actual page exists in the CMS only.
#
# These URLs must have matching routes set up in the CMS pages
# else they can lead to a 404 from the CMS. If the CMS has a translated
# version of that page available in a locale that the user prefers
# (via their Accept-Language header) or in the default
# settings.LANGUAGE_CODE locale, the user will be redirected to that.
#
# Note that all URL routes defined here should point to the
# dummy_view function, which never gets called because this
# urlconf is only use with reverse(), never resolve()


from django.urls import path

from bedrock.base.i18n import bedrock_i18n_patterns


def dummy_view(*args, **kwargs):
    # This view will never get called
    pass


urlpatterns = bedrock_i18n_patterns(
    # pattern is:
    # path("url/path/here/", dummy_view, name="route.name.here"),
    path("about/leadership/", dummy_view, name="mozorg.about.leadership.index"),
    path("products/monitor/", dummy_view, name="products.monitor.landing"),
    path("products/vpn/resource-center/", dummy_view, name="products.vpn.resource-center.landing"),
    path("products/vpn/resource-center/<slug:slug>/", dummy_view, name="products.vpn.resource-center.article"),
    path("advertising/", dummy_view, name="mozorg.advertising.landing"),
)
