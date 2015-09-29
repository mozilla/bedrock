# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import url

import views
import bedrock.releasenotes.views
from bedrock.mozorg.util import page
from bedrock.releasenotes import version_re


latest_re = r'^thunderbird(?:/(?P<version>%s))?/%s/$'
channel_re = '(?P<channel>beta|earlybird)'
notes_re = latest_re % (version_re, r'releasenotes')
sysreq_re = latest_re % (version_re, 'system-requirements')


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
    # FIXME: As you see, the product names are inconsistent due to the current
    # bedrock.releasenotes implementation. Some view methods are tied to the
    # product names in Nucleus, which are "Firefox", "Firefox for Android" and
    # "Thunderbird", so those are not lower-case. We should fix it.
    url(r'^thunderbird/(?:%s/)?all/$' % channel_re,
        views.all_downloads, name='thunderbird.latest.all'),
    url('^thunderbird/releases/$',
        bedrock.releasenotes.views.releases_index,
        {'product': 'Thunderbird'}, name='thunderbird.releases.index'),
    url('^thunderbird/(?:%s/)?notes/$' % channel_re,
        bedrock.releasenotes.views.latest_notes,
        {'product': 'thunderbird'}, name='thunderbird.latest.notes'),
    url('^thunderbird/latest/releasenotes/$',
        bedrock.releasenotes.views.latest_notes,
        {'product': 'thunderbird', 'channel': 'release'}),
    url(notes_re,
        bedrock.releasenotes.views.release_notes,
        {'product': 'Thunderbird'}, name='thunderbird.notes'),
    url('^thunderbird/(?:%s/)?system-requirements/$' % channel_re,
        bedrock.releasenotes.views.latest_sysreq,
        {'product': 'thunderbird'}, name='thunderbird.latest.sysreq'),
    url('^thunderbird/latest/system-requirements/$',
        bedrock.releasenotes.views.latest_sysreq,
        {'product': 'thunderbird', 'channel': 'release'}),
    url(sysreq_re,
        bedrock.releasenotes.views.system_requirements,
        {'product': 'Thunderbird'}, name='thunderbird.sysreq'),
)
