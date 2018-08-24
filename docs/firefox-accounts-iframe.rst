.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _firefox-accounts-iframe:

============================
Firefox Accounts Signup Form
============================

Introduction
------------

Certain bedrock pages such as ``/firefox/accounts`` and ``/firefox/firstrun`` feature a
Firefox Accounts signup form using an embedded ``iframe``. To test the signup flow on
a non-production environment requires some additional Firefox profile configuration.

Demo Server Testing
-------------------

#. Open ``about:profiles``.
#. Click the ``Create a New Profile`` button and enter the profile name ``FxA Test Demo``.
#. Find ``FxA Test Demo`` in the profile list and click ``Launch profile in new browser``.
#. Open ``about:config`` and add a new preference called ``identity.fxaccounts.autoconfig.uri`` with the value ``https://accounts.stage.mozaws.net``.
#. Open ``about:preferences#sync`` and click ``Sign in``.
#. Verify that the sign in page loads from ``https://accounts.stage.mozaws.net/`` (but don't actually sign in).
#. Restart the browser.
#. Navigate to the web page containing the form and test signing up.

Clearing the iframe cache
-------------------------

To clear browser cache while testing multiple accounts, append ``/clear`` to the iframe's
source URL, e.g. ``https://accounts.stage.mozaws.net/clear``

Embedding on a page
-------------------

To embed the Firefox Accounts iframe on a page:

#. Add the FxA JavaScript & Less files to the page's bundles:
    - ``media/js/base/mozilla-fxa-iframe.js``
    - ``media/css/base/mozilla-fxa-iframe.less``
#. Add the following attributes and values to any element on the page (the
   parent element of the ``<iframe>`` is a good option):

    ``id="fxa-iframe-config" data-host="{{ settings.FXA_IFRAME_SRC }}" data-mozillaonline-host="{{ settings.FXA_IFRAME_SRC_MOZILLAONLINE }}"``
#. Add the ``<iframe>`` to the page with the following attributes and values:
    ``<iframe id="fxa" scrolling="no" data-src="{{ settings.FXA_IFRAME_SRC }}?utm_campaign=fxa-embedded-form&amp;utm_content=fx-{{ version }}&amp;service=sync&amp;context=iframe&amp;style=chromeless&amp;haltAfterSignIn=true"></iframe>``

    .. note::

        Note that each implementation of the ``<iframe>`` may require unique URL
        parameters in the ``data-src`` attribute for some or all of the following:

        - ``utm_medium``
        - ``utm_source``
        - ``entrypoint``

.. _instructions here: https://support.mozilla.org/kb/profile-manager-create-and-remove-firefox-profiles
