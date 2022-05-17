.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _vpn_affiliate_attribution:

===================================================================
Mozilla :abbr:`VPN (Virtual Private Network)` Affiliate Attribution
===================================================================

The affiliate attribution flow for the Mozilla :abbr:`VPN (Virtual Private Network)` `landing page`_ comprises
an integration between the `Commission Junction (CJ)`_ affiliate marketing
event system, bedrock, and the :abbr:`VPN (Virtual Private Network)` product team's `CJ micro service (CJMS)`_.
For a more detailed breakdown you can view the `full flow diagram`_, but at
a high level the logic that bedrock is responsible for is as follows:

#. On page load, bedrock looks for a ``cjevent`` query parameter in the page URL.
#. If found, we validate the query param value and then ``POST`` it together
   with a Firefox Account ``flow_id`` to the CJMS.
#. The CJMS responds with an affiliate marketing ID and expiry time, which we
   then set as a first-party cookie. This cookie is used to maintain a
   relationship between the ``cjevent`` value and an individual ``flow_id``,
   so that successful subscriptions can be properly attributed to CJ.
#. If a website visitor later returns to the landing page with an affiliate
   marketing cookie already set, then we update the ``flow_id`` and ``cjevent``
   value (if a new one exists) via ``PUT`` on their repeat visit. This ensures
   that the most recent CJ referral is attributed if/when someone decides to
   purchase a subscription.
#. The CJMS then responds with an updated ID / expiry time for the affiliate
   marketing cookie.
#. To facilitate an opt-out of attribution, we display a cookie notification
   with an opt-out button at the top of the landing page when the flow initiates.
#. If someone clicks "Reject" to opt-out, we generate a new ``flow_id``
   (invalidating the existing ``flow_id`` in the CJMS database) and then delete
   the affiliate marketing cookie, replacing it with a "reject" preference
   cookie that will prevent attribution from initiating on repeat visits.
   This preference cookie will expire after 1 month.
#. If someone clicks "OK" or closes the opt-out notification by clicking the "X"
   icon, here we assume the website visitor is OK with attribution. We set an
   "accept" preference cookie that will prevent displaying the opt-out
   notification on future visits (again with a 1 month expiry) and allow
   attribution to flow.

.. Note::

   To query what version of CJMS is currently deployed at the endpoint bedrock
   points to, you can add ``__version__`` at the end of the base URL to see
   the release number and commit hash. For example:
   https://stage.cjms.nonprod.cloudops.mozgcp.net/__version__

.. _landing page: https://www.mozilla.org/en-US/products/vpn/
.. _Commission Junction (CJ): https://www.cj.com/
.. _CJ micro service (CJMS): https://github.com/mozilla-services/cjms
.. _full flow diagram: https://www.figma.com/file/6jnLCLzclBN0uyS4nJp57d/Affiliate-Marketing-(CJ)-Architecture-%2F-Flow
