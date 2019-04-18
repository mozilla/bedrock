# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.utils.http import urlquote


# Link to Firefox for Android on the Google Play store with Google Analytics
# campaign parameters.
# To clarify below, 'referrer' key value must be a URL encoded string of utm_*
# key/values (https://bugzilla.mozilla.org/show_bug.cgi?id=1099429#c0).
GOOGLE_PLAY_FIREFOX_LINK = ('https://play.google.com/store/apps/details?' +
                            'id=org.mozilla.firefox&referrer=' +
                            urlquote('utm_source=mozilla&utm_medium=Referral&'
                                     'utm_campaign=mozilla-org'))

# Bug 1264843: link to China build of Fx4A, for display within Fx China repack
GOOGLE_PLAY_FIREFOX_LINK_MOZILLAONLINE = GOOGLE_PLAY_FIREFOX_LINK.replace(
    'org.mozilla.firefox', 'cn.mozilla.firefox')

# Link to Firefox for iOS on the Apple App Store with Google Analytics campaign
# patameters. Each implementation should add a "ct" parameter for analytics.
# Note: this URL is likely to change for Fx42. See bug comment:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1196310#c18
APPLE_APPSTORE_FIREFOX_LINK = ('https://itunes.apple.com/{country}/app/' +
                               'apple-store/id989804926?pt=373246&mt=8')

# Map Mozilla's locale codes to Apple's country codes so we can link to a
# localized App Store page when possible. Here's the official territory list:
# https://developer.apple.com/library/ios/documentation/LanguagesUtilities/Conceptual/iTunesConnect_Guide/Appendices/AppStoreTerritories.html
APPLE_APPSTORE_COUNTRY_MAP = {
    'sq': 'al',     # Albania
    'hy-AM': 'am',  # Armenia
    'es-AR': 'ar',  # Argentina
    'az': 'az',     # Azerbaijan
    'bg': 'bg',     # Bulgaria
    'pt-BR': 'br',  # Brazil
    'be': 'by',     # Belarus
    'es-CL': 'cl',  # Chile
    'zh-CN': 'cn',  # China
    'cs': 'cz',     # Czech
    'de': 'de',     # Germany
    'da': 'dk',     # Denmark
    'et': 'ee',     # Estonia
    'es-ES': 'es',  # Spain
    'fi': 'fi',     # Finland
    'fr': 'fr',     # France
    'en-GB': 'gb',  # United Kingdom
    'el': 'gr',     # Greece
    'hr': 'hr',     # Croatia
    'hu': 'hu',     # Hungary
    'id': 'id',     # Indonesia
    'ga-IE': 'ie',  # Ireland
    'he': 'il',     # Israel
    'bn-IN': 'in',  # India
    'gu-IN': 'in',  # India
    'hi-IN': 'in',  # India
    'pa-IN': 'in',  # India
    'is': 'is',     # Iceland
    'it': 'it',     # Italy
    'ja': 'jp',     # Japan
    'ko': 'kr',     # Republic Of Korea
    'kk': 'kz',     # Kazakstan
    'lt': 'lt',     # Lithuania
    'lv': 'lv',     # Latvia
    'mk': 'mk',     # Macedonia
    'es-MX': 'mx',  # Mexico
    'ms': 'my',     # Malaysia
    'nl': 'nl',     # Netherlands
    'nb-NO': 'no',  # Norway
    'nn-NO': 'no',  # Norway
    'pl': 'pl',     # Poland
    'pt-PT': 'pt',  # Portugal
    'ro': 'ro',     # Romania
    'ru': 'ru',     # Russia
    'sv-SE': 'se',  # Sweden
    'sl': 'si',     # Slovenia
    'sk': 'sk',     # Slovakia
    'th': 'th',     # Thailand
    'tr': 'tr',     # Turkey
    'zh-TW': 'tw',  # Taiwan
    'uk': 'ua',     # Ukraine
    'en-US': 'us',  # United States
    'uz': 'uz',     # Uzbekistan
    'vi': 'vt',     # Vietnam
}

# Link to Firefox Focus for iOS on the Apple App Store via app.adjust.
# Fallback parameter sends users who are on the wrong platform to the iTunes website.
# https://bugzilla.mozilla.org/show_bug.cgi?id=1350170
APPLE_APPSTORE_FIREFOX_FOCUS_LINK = ('https://app.adjust.com/b8s7qo?campaign=moz.org&adgroup=Focus&creative=iOS&' +
                                     'fallback=https%3A%2F%2Fitunes.apple.com%2Fapp%2Fid1055677337%3Fmt%3D8')

# Link to Firefox Focus for Android on the Google Play Store via app.adjust.
# Fallback parameter sends users who are on the wrong platform to the Play Store website.
# https://bugzilla.mozilla.org/show_bug.cgi?id=1350170
GOOGLE_PLAY_FIREFOX_FOCUS_LINK = ('https://app.adjust.com/b8s7qo?campaign=moz.org&adgroup=Focus&creative=android' +
                                  '&fallback=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%2Fdetails%3Fid%3Dorg.mozilla.focus')
