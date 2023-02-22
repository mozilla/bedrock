.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _firefox_stub_attribution:

========================
Firefox Stub Attribution
========================

Stub Attribution is a process that enables the construction and transmission
of marketing attribution code for Firefox desktop on www.mozilla.org. When a user
visits a mozilla.org download page, the website constructs an attribution code,
which is then passed to download.mozilla.org via a URL parameter. This attribution
code is then passed to the Windows stub installer, where it finally gets passed to
Firefox for use in Telemetry. This attribution funnel enables Mozilla to better
understand how different marketing campaigns effect overall retention in Firefox.

How does it work in bedrock?
----------------------------

The base template in bedrock contains a stub attribution script that runs on every
page of the website. The script only runs on Windows (since the stub installer is a
Windows feature) and if cookies are enabled. The script also respects Do Not Track,
so it will not run if the user agent has this flag set.

The stub attribution script looks for ``utm_*`` params on the page URL, as well
``document.referrer`` and various other values, and then creates a hash of that
data by passing it to an authentication service in bedrock. This hash is then
accompanied by a signed, encrypted signature to prove that the data came from a
trusted source. Both pieces of authenticated data are then stored in a cookie with
a 24 hour expiry.

The full list of data values we pass to stub attribution is as follows:

- ``utm_source`` (``?utm_source=`` query parameter)
- ``utm_medium`` (``?utm_medium=`` query parameter)
- ``utm_campaign`` (``?utm_campaign=`` query parameter)
- ``utm_content`` (``?utm_content=`` query parameter)
- ``referrer`` (``document.referrer``)
- ``ua`` (simplified browser name parsed from UA string, e.g. ``chrome``, ``safari``, ``firefox``).
- ``experiment`` (``?experiment=`` query parameter)
- ``variation`` (``?variation=`` query parameter)
- ``visit_id`` (``clientId`` client ID from Google Analytics)
- ``session_id`` (``_gt`` session ID from Google Analytics)

.. Note::

    If any of the above values are not present then a default value of ``(not set)``
    will be used.

The cookies created during the stub attribution flow are called:

- ``moz-stub-attribution-code`` (base64 encoded attribution data string)
- ``moz-stub-attribution-sig`` (encrypted signature)

Once the user reaches the download page, bedrock then checks if the cookie exists,
and if so appends the authenticated data to the download URL. The query parameters
added to the download URLs are labeled as:

- ``attribution_code`` (value of ``moz-stub-attribution-code``)
- ``attribution_sig`` (value of ``moz-stub-attribution-sig``)

Once a visitor clicks the download link, the rest of the process is handled by the
download service and stub installer.

Local testing
-------------

For stub attribution to work locally or on a demo instance, a value for the HMAC key
that is used to sign the attribution code must be set via an environment variable e.g.

.. code-block:: html

    STUB_ATTRIBUTION_HMAC_KEY=thedude

.. Note::

    This value can be anything if all you need to do is test the bedrock functionality.
    It only needs to match the value used to verify data passed to the stub installer
    for full end-to-end testing via Telemetry.

Measuring campaigns and experiments
-----------------------------------

Stub Attribution was originally designed for measuring the effectiveness of marketing
campaigns where the top of the funnel was outside the remit of www.mozilla.org. For
these types of campaigns, stub attribution requires zero configuration. It just works
(as configured in  ``/media/js/base/stub-attribution.js``) in the background and passes
along any attribution data that exists.

More recently, the ability to measure the effectiveness of experiments was also added
as a feature. This is achieved by adding optional ``experiment`` and ``variation``
parameters to a page URL. Additionally, these values can also be set via JavaScript
using:

.. code-block:: javascript

    Mozilla.StubAttribution.experimentName = 'experiment-name';
    Mozilla.StubAttribution.experimentVariation = 'v1';

.. Note::

    When setting a experiment parameters using JavaScript like in the example above,
    it must be done prior to calling ``Mozilla.StubAttribution.init()``.

Return to addons.mozilla.org (RTAMO)
------------------------------------

`Return to AMO`_ (RTAMO) is a Firefox feature whereby a first-time installation onboarding
flow is initiated, that redirects a user to install the extension they have chosen whilst
browsing `AMO`_ using a different browser. RTAMO works by leveraging the existing stub
attribution flow, and checking for specific ``utm_`` parameters that were passed if the
referrer is from AMO.

Specifically, the RTAMO feature looks for a ``utm_content`` parameter that starts with ``rta:``,
followed by an ID specific to an extension. For example: ``utm_content=rta:dUJsb2NrMEByYXltb25kaGlsbC5uZXQ``.
The stub attribution code in bedrock also checks the referrer before passing this on, to
make sure the links originate from AMO. If RTAMO data comes from a domain other than AMO, then the
attribution data is dropped.

RTAMO initially worked for only a limited subset of addons recommended by Mozilla. This
functionality was recently expanded by the AMO team to cover all publically listed addons,
under a project called `Extended RTAMO (ERTAMO)`.

.. _AMO: https://addons.mozilla.org/firefox/
.. _Return to AMO: https://wiki.mozilla.org/Add-ons/QA/Testplan/Return_to_AMO
