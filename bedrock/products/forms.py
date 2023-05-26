# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.newsletter.forms import NewsletterFooterForm


class VPNWaitlistForm(NewsletterFooterForm):
    def __init__(self, locale, data=None, *args, **kwargs):
        super().__init__("guardian-vpn-waitlist", locale, data, *args, **kwargs)


class RelayBundleWaitlistForm(NewsletterFooterForm):
    def __init__(self, locale, data=None, *args, **kwargs):
        super().__init__("relay-vpn-bundle-waitlist", locale, data, *args, **kwargs)


class RelayPhoneWaitlistForm(NewsletterFooterForm):
    def __init__(self, locale, data=None, *args, **kwargs):
        super().__init__("relay-phone-masking-waitlist", locale, data, *args, **kwargs)
