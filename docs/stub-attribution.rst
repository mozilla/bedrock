.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _stub_attribution:

================
Stub Attribution
================

Stub Attribution is a process that enables the construction and transmission
of marketing attribution code on www.mozilla.org. When a user visits a mozilla.org
download page, the website constructs an attribution code, which is then passed to
download.mozilla.org via a URL parameter. This attribution code is then passed to
the Windows stub installer, where it finally gets passed to Firefox for use in
Telemetry. This attribution funnel enables Mozilla to better understand how
different marketing campaigns effect overall retention in Firefox.

.. Note::

    The `AMO`_ team also relies on Stub Attribution on the /new page to inform
    their `Return to AMO`_ feature.

How does it work in bedrock?
----------------------------

The base template in bedrock contains a stub attribution script that runs on every
page of the website. The script only runs on Windows (since the stub installer is a
Windows feature) and if cookies are enabled. The script also respects Do Not Track,
so it will not run if the user agent has this flag set.

The stub attribution script looks for `utm_*` params on the page URL as well as the
referrer, and then creates a hash of that data by passing it to an authentication
service in bedrock. This hash is then accompanied by a signed, encrypted signature
to prove that the data came from a trusted source. Both pieces of authenticated
data are then stored in a cookie.

Once the user reaches the download page, bedrock then checks if the cookie exists,
and if so appends the authenticated data to the download URL. The rest of the process
is handled by the download service and stub installer.

Local testing
-------------

For stub attribution to work locally or on a demo instance, a value for the HMAC key
that is used to sign the attribution code must be set via an environment variable e.g.

.. code-block:: html

    STUB_ATTRIBUTION_HMAC_KEY='thedude'

.. Note::

    This value can be anything if all you need to do is test the bedrock functionality.
    It only needs to match the value used to verify data passed to the stub installer
    for full end-to-end testing via Telemetry.

Measuring campaigns and experiments
-----------------------------------

Stub Attribution was originally designed for measuring the effectiveness of marketing
campaigns where the top of the funnel was outside the remit of www.mozilla.org. For
these types of campaigns, stub attribution requires zero configuration. It just works
(as configured in  `/media/js/base/stub-attribution.js`) in the background and passes
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

.. _AMO: https://addons.mozilla.org/firefox/
.. _Return to AMO: https://wiki.mozilla.org/Add-ons/QA/Testplan/Return_to_AMO
