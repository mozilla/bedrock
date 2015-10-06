# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from bedrock.redirects.util import redirect
from bedrock.mozorg.util import page


urlpatterns = (
    # There will eventually be a main education landing page
    # but we'll redirect until then.
    redirect(r'^teach/$', 'teach.smarton.security', name='teach'),

    # There will eventually be a main SmartOn landing page
    # but we'll redirect until then.
    redirect(r'^teach/smarton/$', 'teach.smarton.security', name='teach.smarton'),

    # SmartOn
    page('teach/smarton/tracking', 'teach/smarton/tracking.html'),
    page('teach/smarton/security', 'teach/smarton/security.html'),
)
