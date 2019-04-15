from __future__ import absolute_import
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url
from bedrock.mozorg.util import page

from . import views


urlpatterns = (
    page('firefox/retention/thank-you-a', 'etc/firefox/retention/thank-you-a.html'),
    page('firefox/retention/thank-you-b', 'etc/firefox/retention/thank-you-b.html'),
    url(r'^firefox/retention/thank-you-referral/$',
        views.ThankyouView.as_view(),
        name='firefox.retention.thank-you-referral'),
)
