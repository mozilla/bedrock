# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from urllib.parse import quote

# Base link to Firefox for Android on the Google Play store.
GOOGLE_PLAY_FIREFOX_LINK = "https://play.google.com/store/apps/details?id=org.mozilla.firefox"

# Link to Firefox for Android on the Google Play store with Google Analytics
# campaign parameters.
# To clarify below, 'referrer' key value must be a URL encoded string of utm_*
# key/values (https://bugzilla.mozilla.org/show_bug.cgi?id=1099429#c0).
GOOGLE_PLAY_FIREFOX_LINK_UTMS = GOOGLE_PLAY_FIREFOX_LINK + "&referrer=" + quote("utm_source=mozilla&utm_medium=Referral&utm_campaign=mozilla-org")

# Bug 1264843, Issue 13108: link to China build of Fx4A, for display within Fx China repack
GOOGLE_PLAY_FIREFOX_LINK_MOZILLAONLINE = "https://www.firefox.com.cn/mobile/get-app/"

# Link to Firefox for iOS on the Apple App Store.
APPLE_APPSTORE_FIREFOX_LINK = "https://apps.apple.com/{country}/app/apple-store/id989804926"

# Map Mozilla's locale codes to Apple's country codes so we can link to a
# localized App Store page when possible. Here's the official territory list:
# https://developer.apple.com/library/ios/documentation/LanguagesUtilities/Conceptual/iTunesConnect_Guide/Appendices/AppStoreTerritories.html
APPLE_APPSTORE_COUNTRY_MAP = {
    "sq": "al",  # Albania
    "hy-AM": "am",  # Armenia
    "es-AR": "ar",  # Argentina
    "az": "az",  # Azerbaijan
    "bg": "bg",  # Bulgaria
    "pt-BR": "br",  # Brazil
    "be": "by",  # Belarus
    "es-CL": "cl",  # Chile
    "zh-CN": "cn",  # China
    "cs": "cz",  # Czech
    "de": "de",  # Germany
    "da": "dk",  # Denmark
    "et": "ee",  # Estonia
    "es-ES": "es",  # Spain
    "fi": "fi",  # Finland
    "fr": "fr",  # France
    "en-GB": "gb",  # United Kingdom
    "el": "gr",  # Greece
    "hr": "hr",  # Croatia
    "hu": "hu",  # Hungary
    "id": "id",  # Indonesia
    "ga-IE": "ie",  # Ireland
    "he": "il",  # Israel
    "bn-IN": "in",  # India
    "gu-IN": "in",  # India
    "hi-IN": "in",  # India
    "pa-IN": "in",  # India
    "is": "is",  # Iceland
    "it": "it",  # Italy
    "ja": "jp",  # Japan
    "ko": "kr",  # Republic Of Korea
    "kk": "kz",  # Kazakstan
    "lt": "lt",  # Lithuania
    "lv": "lv",  # Latvia
    "mk": "mk",  # Macedonia
    "es-MX": "mx",  # Mexico
    "ms": "my",  # Malaysia
    "nl": "nl",  # Netherlands
    "nb-NO": "no",  # Norway
    "nn-NO": "no",  # Norway
    "pl": "pl",  # Poland
    "pt-PT": "pt",  # Portugal
    "ro": "ro",  # Romania
    "ru": "ru",  # Russia
    "sv-SE": "se",  # Sweden
    "sl": "si",  # Slovenia
    "sk": "sk",  # Slovakia
    "th": "th",  # Thailand
    "tr": "tr",  # Turkey
    "zh-TW": "tw",  # Taiwan
    "uk": "ua",  # Ukraine
    "en-US": "us",  # United States
    "uz": "uz",  # Uzbekistan
    "vi": "vt",  # Vietnam
}

# Link to Firefox Focus on the Apple App Store.
APPLE_APPSTORE_FOCUS_LINK = "https://apps.apple.com/{country}/app/apple-store/id1055677337"

# Link to Firefox Focus on the Google Play store.
GOOGLE_PLAY_FOCUS_LINK = "https://play.google.com/store/apps/details?id=org.mozilla.focus"

# Link to Firefox Focus on the Apple App Store.
APPLE_APPSTORE_KLAR_LINK = "https://apps.apple.com/{country}/app/apple-store/id1073435754"

# Link to Firefox Klar on the Google Play store.
GOOGLE_PLAY_KLAR_LINK = "https://play.google.com/store/apps/details?id=org.mozilla.klar"

# Link to Pocket on the Apple App Store.
APPLE_APPSTORE_POCKET_LINK = "https://apps.apple.com/{country}/app/apple-store/id309601447"

# Link to Pocket on the Google Play store.
GOOGLE_PLAY_POCKET_LINK = "https://play.google.com/store/apps/details?id=com.ideashower.readitlater.pro"

# Link to Firefox Beta on the Google Play Store.
GOOGLE_PLAY_FIREFOX_BETA_LINK = "https://play.google.com/store/apps/details?id=org.mozilla.firefox_beta"

# Link to Firefox Nightly on the Google Play Store.
GOOGLE_PLAY_FIREFOX_NIGHTLY_LINK = "https://play.google.com/store/apps/details?id=org.mozilla.fenix"

# Link to Firefox for Fire TV on Amazon Store.
AMAZON_FIREFOX_FIRE_TV_LINK = "https://www.amazon.com/Mozilla-Firefox-for-Fire-TV/dp/B078B5YMPD"

# Link to Firefox Send on the Google Play Store.
GOOGLE_PLAY_FIREFOX_SEND_LINK = "https://play.google.com/store/apps/details?id=org.mozilla.firefoxsend"
