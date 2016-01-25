# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils

from bedrock.thunderbird.details import thunderbird_desktop


def all_downloads(request, channel):
    if channel is None:
        channel = 'release'
    if channel == 'earlybird':
        channel = 'alpha'

    version = thunderbird_desktop.latest_version(channel)
    query = request.GET.get('q')

    context = {
        'platform': 'desktop',
        'platforms': thunderbird_desktop.platforms(channel),
        'full_builds_version': version.split('.', 1)[0],
        'full_builds': thunderbird_desktop.get_filtered_full_builds(channel, version, query),
        'query': query,
        'channel': channel,
        'channel_label': thunderbird_desktop.channel_labels.get(channel, 'Thunderbird'),
    }

    return l10n_utils.render(request, 'thunderbird/all.html', context)
