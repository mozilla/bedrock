# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.redirects.util import redirect

redirectpatterns = (
    # bug 926629
    redirect(r"^newsletter/about_mobile(?:/(?:index\.html)?)?$", "newsletter.subscribe"),
    redirect(r"^newsletter/about_mozilla(?:/(?:index\.html)?)?$", "mozorg.contribute"),
    redirect(r"^newsletter/new(?:/(?:index\.html)?)?$", "newsletter.subscribe"),
    redirect(r"^newsletter/ios(?:/(?:index\.html)?)?$", "firefox.browsers.mobile.ios"),
    redirect(r"^newsletter/country/success/?$", "newsletter.updated"),
)
