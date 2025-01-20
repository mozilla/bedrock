# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# This module contains named URL paths which only exist in the CMS.
#
# They are named so that they can be looked up via our url() jinja
# helper, even though the actual page exists in the CMS only.
#
# These URLs will/must have matching routes set up in the CMS pages
# else they will lead to a 404 from the CMS.
#
# Note that all URL routes defined here should point to the
# dummy_view function, which never gets called because this
# urlconf is only use with reverse(), never resolve()


# from django.urls import path


def dummy_view(*args, **kwargs):
    # This view will never get called
    pass


urlpatterns = (
    # pattern is:
    # path("url/path/here/", dummy_view, name="route.name.here"),
)
