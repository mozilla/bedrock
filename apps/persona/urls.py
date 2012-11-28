# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls.defaults import *
from mozorg.util import page

urlpatterns = patterns('',
    page('', 'persona/persona.html'),
    page('about', 'persona/about.html'),
    page('privacy-policy', 'persona/privacy-policy.html'),
    page('terms-of-service', 'persona/terms-of-service.html'),
    page('developer-faq', 'persona/developer-faq.html')
)
