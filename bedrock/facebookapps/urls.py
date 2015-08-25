# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf.urls import url

from commonware.decorators import xframe_allow

from bedrock.facebookapps import views
from bedrock.facebookapps.decorators import extract_app_data, facebook_locale
from bedrock.mozorg.util import page


urlpatterns = (
    url(r'^tab_redirect/$', views.tab_redirect,
        name='facebookapps.tab_redirect'),
    url(r'^tab_redirect/(?P<redirect_type>[a-z]*)/$', views.tab_redirect,
        name='facebookapps.tab_redirect'),

    page('channel', 'facebookapps/channel.html'),
    page('downloadtab', 'facebookapps/downloadtab.html',
        decorators=(xframe_allow, extract_app_data, facebook_locale)),
    page('downloadtab/noscroll', 'facebookapps/downloadtab.html',
        decorators=(xframe_allow, extract_app_data, facebook_locale),
        noscroll=True),
)
