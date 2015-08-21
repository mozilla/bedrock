# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.conf.urls import patterns, url

import views
import bedrock.releasenotes.views
from bedrock.releasenotes import version_re
from bedrock.mozorg.util import page


latest_re = r'^thunderbird(?:/(?P<version>%s))?/%s/$'
thunderbird_releasenotes_re = latest_re % (version_re, r'releasenotes')
sysreq_re = latest_re % (version_re, 'system-requirements')
channel_re = '(?P<channel>beta|earlybird)'


urlpatterns = patterns('',
    url(r'^thunderbird/(?:%s/)?all/$' % channel_re,
        views.all_downloads, name='thunderbird.all'),

    url('^thunderbird/releases/$', bedrock.releasenotes.views.releases_index,
        {'product': 'Thunderbird'}, name='thunderbird.releases.index'),

    url(thunderbird_releasenotes_re, bedrock.releasenotes.views.release_notes,
        {'product': 'Thunderbird'}, name='thunderbird.releasenotes'),

    url(sysreq_re, bedrock.releasenotes.views.system_requirements,
        {'product': 'Thunderbird'}, name='thunderbird.system_requirements'),

    url('^thunderbird/latest/system-requirements/$',
        bedrock.releasenotes.views.latest_sysreq,
        {'product': 'thunderbird', 'channel': 'release'}, name='thunderbird.sysreq'),

    url('^thunderbird/latest/releasenotes/$',
        bedrock.releasenotes.views.latest_notes,
        {'product': 'thunderbird'}, name='thunderbird.notes'),

    page('thunderbird', 'thunderbird/index.html'),
    page('thunderbird/features', 'thunderbird/features.html'),
    page('thunderbird/email-providers', 'thunderbird/email-providers.html'),

    # Start pages by channel
    page('thunderbird/release/start', 'thunderbird/start/release.html'),
)
