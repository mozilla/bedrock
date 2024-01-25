.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _firefox_mobile_attribution:

==========================
Firefox mobile attribution
==========================

For Firefox mobile referrals we use native app store web links with additional
campaign parameters to help measure download to install rates.

App store url helpers
---------------------

To help streamline creating app store referral links we have `app_store_url()` and
`play_store_url()` helpers, which accept a `product`` name and an optional
`campaign`` parameter.

For example:

```
play_store_url('firefox', 'firefox-home')
app_store_url('firefox', 'firefox-home')
```

Would render:

```
https://apps.apple.com/us/app/apple-store/id989804926?pt=373246&ct=firefox-home&mt=8
https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-home&hl=en
```

For Firefox Focus:

```
play_store_url('focus', 'firefox-browsers-mobile-focus')
app_store_url('focus', 'firefox-browsers-mobile-focus')
```

Would render:

```
https://apps.apple.com/us/app/apple-store/id1055677337?pt=373246&ct=firefox-home&mt=8
https://play.google.com/store/apps/details?id=org.mozilla.focus&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-home&hl=en
```
