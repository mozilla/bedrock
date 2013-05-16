# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from bedrock.firefox.firefox_details import firefox_details


def latest_firefox_versions(request):
    return {
        'latest_firefox_version': firefox_details.latest_version('release'),
        'esr_firefox_versions': firefox_details.esr_major_versions,
    }
