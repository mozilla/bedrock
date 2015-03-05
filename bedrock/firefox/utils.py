# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from product_details import product_details
from product_details.version_compare import Version
from bedrock.firefox.firefox_details import firefox_desktop


def is_current_or_newer(user_version):
    """
    Return true if the version (X.Y only) is for the latest Firefox or newer.
    """
    latest = Version(product_details.firefox_versions[
        'LATEST_FIREFOX_VERSION'])
    user = Version(user_version)

    # check for ESR
    if user.major in firefox_desktop.esr_major_versions:
        return True

    # similar to the way comparison is done in the Version class,
    # but only using the major and minor versions.
    latest_int = int('%d%02d' % (latest.major, latest.minor1))
    user_int = int('%d%02d' % (user.major or 0, user.minor1 or 0))
    return user_int >= latest_int
