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

.. code-block:: jinja

    play_store_url('firefox', 'firefox-home')
    app_store_url('firefox', 'firefox-home')

Would render:

.. code-block::

    https://apps.apple.com/us/app/apple-store/id989804926?pt=373246&ct=firefox-home&mt=8
    https://play.google.com/store/apps/details?id=org.mozilla.firefox&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-home&hl=en

For Firefox Focus:

.. code-block:: jinja

    play_store_url('focus', 'firefox-browsers-mobile-focus')
    app_store_url('focus', 'firefox-browsers-mobile-focus')

Would render:

.. code-block::

    https://apps.apple.com/us/app/apple-store/id1055677337?pt=373246&ct=firefox-home&mt=8
    https://play.google.com/store/apps/details?id=org.mozilla.focus&referrer=utm_source%3Dwww.mozilla.org%26utm_medium%3Dreferral%26utm_campaign%3Dfirefox-home&hl=en

App store redirects
-------------------

Occasionally we need to create a link that can auto redirect to either the Apple
App Store or the Google Play Store depending on user agent. A common use case is
to embed inside a QR Code, which people can then scan on their phone to get a
shortcut to the app. To make this easier bedrock has a special redirect URL to
which you can add product and campaign query strings. When someone hits the
redirect URL, bedrock will attempt to detect their mobile platform and then auto
redirect to the appropriate app store.

The base redirect URL is ``https://www.mozilla.org/firefox/browsers/mobile/app/``,
and to it you can add both a ``product`` and ``campaign`` query parameter. For
example, the following URL would redirect to either Firefox on the Apple App Store
or on the Google Play Store, with the specified campaign parameter.

.. code-block::

    https://www.mozilla.org/firefox/browsers/mobile/app/?product=firefox&campaign=firefox-whatsnew

.. note::

    The ``product`` and ``campaign`` parameters are limited to a set of strictly
    trusted values. To add more product and campaign options, you can add those
    values to the ``mobile_app`` helper function in
    `firefox/redirects.py <https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/redirects.py>`_.

Where can I find mobile attribution data?
-----------------------------------------

You can find Firefox Android client attribution data in `Looker`_. Firefox iOS data
is currently only available in `App Store Connect`_, however this will also be added to
Looker in the near future.

.. _Looker: https://mozilla.cloud.looker.com/looks/1997
.. _App Store Connect: https://appstoreconnect.apple.com/
