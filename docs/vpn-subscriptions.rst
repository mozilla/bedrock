.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _vpn_subscriptions:

=========================
Mozilla VPN Subscriptions
=========================

Most of the logic to do with VPN lives with the VPN-specific product pages.
However, pages in the `firefox` app may sometimes need some VPN-related
settings, such as for a What's New page.

Excluded countries
------------------

For a list of country codes where we are legally obligated to prevent purchasing VPN,
see ``VPN_EXCLUDED_COUNTRY_CODES`` in ``bedrock/settings/base.py``.

.. _Mozilla VPN landing page: https://www.mozilla.org/en-US/products/vpn/
.. _VPN wait list: https://www.mozilla.org/en-US/products/vpn/invite/
.. _ISO country codes: https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements
.. _ISO 4217 currency codes: https://en.wikipedia.org/wiki/ISO_4217#Active_codes
.. _unit tests: https://github.com/mozilla/bedrock/blob/main/bedrock/products/tests/test_helper_misc.py
