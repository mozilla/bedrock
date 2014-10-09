# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from product_details import product_details
from product_details.version_compare import Version
from bedrock.firefox import version_re
from bedrock.firefox.firefox_details import firefox_details


UA_REGEXP = re.compile(r"Firefox/(%s)" % version_re)

def is_current_or_newer(user_version):
    """
    Return true if the version (X.Y only) is for the latest Firefox or newer.
    """
    latest = Version(product_details.firefox_versions[
        'LATEST_FIREFOX_VERSION'])
    user = Version(user_version)

    # check for ESR
    if user.major in firefox_details.esr_major_versions:
        return True

    # similar to the way comparison is done in the Version class,
    # but only using the major and minor versions.
    latest_int = int('%d%02d' % (latest.major, latest.minor1))
    user_int = int('%d%02d' % (user.major or 0, user.minor1 or 0))
    return user_int >= latest_int

def is_firefox(user_agent):
    """
    Checks user agent string to determine if browser is Firefox.
    """
    # 'Firefox' should be in user_agent
    matchFx = re.compile('(.*?)Firefox(.*?)').search(user_agent)
    # all below tests should return None
    matchLikeFx = re.compile('(.*?)like Firefox(.*?)',
        re.IGNORECASE).search(user_agent)
    matchIceweasel = re.compile('(.*?)Iceweasel(.*?)',
        re.IGNORECASE).search(user_agent)
    matchSeamonkey = re.compile('(.*?)SeaMonkey(.*?)',
        re.IGNORECASE).search(user_agent)

    if (matchFx and not matchLikeFx and not matchIceweasel
        and not matchSeamonkey):

        return True
    else:
        return False

def firefox_version(user_agent):
    """
    Extracts the Firefox version from the given user agent string.
    """
    fx_version = '0'

    if is_firefox(user_agent):
        match = UA_REGEXP.search(user_agent)
        if match:
            fx_version = match.group(1)

    return fx_version
