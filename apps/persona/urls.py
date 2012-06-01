# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from views import persona, about, developerfaq, termsofservice, privacypolicy

urlpatterns = patterns('',
    (r'^developer-faq/$', developerfaq),
    (r'^terms-of-service/$', termsofservice),
    (r'^privacy-policy/$', privacypolicy),
    (r'^about/$', about),
    (r'^$', persona),
)
