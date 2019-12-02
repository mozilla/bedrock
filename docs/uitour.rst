.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _ui-tour:

==============
Mozilla.UITour
==============

Introduction
------------

``Mozilla.UITour`` is a JS library that exposes an event-based Web API for
communicating with the Firefox browser chrome. It can be used for tasks such
as opening menu panels, highlighting buttons, or querying Firefox Account
signed-in state. It is supported in Firefox 29 onward, but some API calls
are only supported in later versions.

For security reasons ``Mozilla.UITour`` will only work on white-listed domains
and over a secure connection. The list of allowed origins can be found here:
https://searchfox.org/mozilla-central/source/browser/app/permissions

The ``Mozilla.UITour`` library is maintained on `Mozilla Central`_.

.. Important::

    The API is supported only on the desktop versions of Firefox. It doesn't
    work on Firefox for Android and iOS.

Local development
-----------------

To develop or test using Mozilla.UITour locally you need to create some custom
preferences in ``about:config``.

* ``browser.uitour.testingOrigins`` (string) (value: local address e.g. ``http://127.0.0.1:8000``)
* ``browser.uitour.requireSecure`` (boolean) (value: ``false``)

Note that ``browser.uitour.testingOrigins`` can be a comma separated list of domains, e.g.

    'http://127.0.0.1:8000, https://www-demo2.allizom.org'

.. Important::

    Prior to Firefox 36, the testing preference was called ``browser.uitour.whitelist.add.testing``
    (Bug 1081772). This old preference does not accept a comma separated list of domains, and you
    must also exclude the domain protocol e.g. ``https://``. A browser restart is also required
    after adding a whitelisted domain.

JavaScript API
--------------

The UITour API documentation can be found in the `Mozilla Source Tree Docs`_.

.. _Mozilla Source Tree Docs: https://firefox-source-docs.mozilla.org/browser/components/uitour/docs/UITour-lib.html
.. _Mozilla Central: http://dxr.mozilla.org/mozilla-central/source/browser/components/uitour/UITour-lib.js
