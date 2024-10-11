.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _consent_management:

=================================
Managing Data Privacy and Consent
=================================

Please see the internal `Confluence page`_ on Mozilla's overall approach to
handling data privacy and cookie consent management on www.mozilla.org. This
page will include detailed legal guidance and FAQs on the permitted use of
tracking technologies.

Here we will cover bedrock's technical approach to implementing data consent
per that legal guidance, whilst also balancing UX considerations
and input from other teams.

In `EU and EAA countries`_ where explicit consent to cookies and analytics
is required, there are certain web page URLs where bedrock will display
a cookie consent banner. These URLs are stored in a strict `allow-list`_. URLs
that are not in this list will neither show a banner, nor load any non-necessary
cookies / analytics in the EU/EAA. The intent here is to provide as little
disruption for our website visitors as possible, whilst still allowing opt-in
to analytics URLs such as campaign pages. It is also possible to force the banner
to show on any EU page by adding a query parameter `?mozcb=y` (used for specific
campaign traffic sources such as advertisements).

Visitors in the EU/EAA countries can also send an opt-out signal by enabling
either `Global Privacy Control`_ (GPC) and `Do Not Track`_ (DNT) in their
browser. If either of these signals are enabled then we do not show a banner.
Individual cookie preferences can also be updated via a dedicated
`cookie settings page`_ linked in the main footer.

In non-EU/EAA countries, non-necessary cookies and analytics are loaded
by default. Visitors can still opt out via the `cookie settings page`_.
Enabling GPC / DNT will also act as an opt-out signal where needed.

There is a `Figma flowchart`_ detailing the general flow of logic. The code
that implements this logic can be found in the ``media/js/base/consent``
directory.

.. _Confluence page: https://mozilla-hub.atlassian.net/wiki/spaces/EN/pages/538050566/Cookie+Banner+Implementation+On+Mozilla.org
.. _EU and EAA countries: https://www.gov.uk/eu-eea
.. _allow-list: https://github.com/mozilla/bedrock/tree/main/media/js/base/consent/allow-list.es6.js
.. _Global Privacy Control: https://developer.mozilla.org/docs/Web/API/Navigator/globalPrivacyControl
.. _Do Not Track: https://developer.mozilla.org/docs/Web/API/Navigator/doNotTrack
.. _cookie settings page: https://www.mozilla.org/privacy/websites/cookie-settings/
.. _Figma flowchart: https://www.figma.com/file/DRdAbRUqi2EYynCx13dTfB/www.mozilla.org-cookie---Cookie-Consent-Flowchart?type=whiteboard&node-id=0%3A1&t=GbhFf7ZCC5XcQR29-1

Related dependencies
--------------------

For more detail documentation on dependencies used for consent management,
see their respective GitHub repositories.

- `Cookie consent banner repo`_
- `Cookie helper repo`_
- `DNT helper repo`_

.. _Cookie consent banner repo: https://github.com/mozmeao/consent-banner/
.. _Cookie helper repo: https://github.com/mozmeao/cookie-helper/
.. _DNT helper repo: https://github.com/mozmeao/dnt-helper/
