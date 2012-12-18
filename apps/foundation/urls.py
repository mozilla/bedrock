# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from mozorg.util import page


urlpatterns = patterns('',
    page('annualreport/2011', 'foundation/annualreport/2011.html'),
    page('annualreport/2011/faq', 'foundation/annualreport/2011faq.html'),
)
