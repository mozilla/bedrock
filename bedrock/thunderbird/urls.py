# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

import views
import bedrock.releasenotes.views
from bedrock.mozorg.util import page


latest_re = r'^thunderbird(?:/(?P<version>%s))?/%s/$'
channel_re = '(?P<channel>beta|earlybird)'


urlpatterns = (
    page('thunderbird', 'thunderbird/index.html'),
    page('thunderbird/features', 'thunderbird/features.html'),
    page('thunderbird/email-providers', 'thunderbird/email-providers.html'),
    page('thunderbird/organizations', 'thunderbird/organizations.html'),
    page('thunderbird/channel', 'thunderbird/channel.html'),

    # Start pages by channel
    page('thunderbird/release/start', 'thunderbird/start/release.html'),
    page('thunderbird/beta/start', 'thunderbird/start/beta.html'),
    page('thunderbird/earlybird/start', 'thunderbird/start/earlybird.html'),
    page('thunderbird/nightly/start', 'thunderbird/start/daily.html'),

    # What's New pages by channel
    page('thunderbird/earlybird/whatsnew', 'thunderbird/whatsnew/earlybird.html'),
    page('thunderbird/nightly/whatsnew', 'thunderbird/whatsnew/daily.html'),

    # Release-related pages
    url(r'^thunderbird/(?:%s/)?all/$' % channel_re,
        views.all_downloads, name='thunderbird.all'),
    url('^thunderbird/releases/$',
        bedrock.releasenotes.views.releases_index,
        {'product': 'Thunderbird'}, name='thunderbird.releases.index'),
    url('^thunderbird/(?:%s/)?notes/$' % channel_re,
        bedrock.releasenotes.views.latest_notes,
        {'product': 'Thunderbird'}, name='thunderbird.notes'),
    url('^thunderbird/latest/releasenotes/$',
        bedrock.releasenotes.views.latest_notes,
        {'product': 'thunderbird', 'channel': 'release'}),
    url('^thunderbird/(?:%s/)?system-requirements/$' % channel_re,
        bedrock.releasenotes.views.latest_sysreq,
        {'product': 'Thunderbird'}, name='thunderbird.sysreq'),
    url('^thunderbird/latest/system-requirements/$',
        bedrock.releasenotes.views.latest_sysreq,
        {'product': 'thunderbird', 'channel': 'release'}),
)
