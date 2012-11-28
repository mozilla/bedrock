# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *

from mozorg.util import page

urlpatterns = patterns('',
    # /apps is temporarily redirected to /apps/partners as per
    # https://bugzilla.mozilla.org/show_bug.cgi?id=751903
    page('', 'marketplace/marketplace.html'),
)
