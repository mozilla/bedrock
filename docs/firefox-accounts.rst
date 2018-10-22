.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _firefox-accounts:

============================
Firefox Accounts Signup Form
============================

Introduction
------------

Certain bedrock pages may feature a Firefox Accounts signup form. As this form has conditional functionality based
on distribution (e.g. the China re-pack), the form should only be displayed to users of Firefox 48 and up.

.. note::

    Firefox 48 is the minimum version needed to support the ``distribution`` property from UITour (which is how
    we detect the China re-pack).


Testing the signup flow on a non-production environment requires additional steps.

Configuring bedrock
-------------------

Set the following in your local ``.env`` file:

``FXA_ENDPOINT=https://latest.dev.lcip.org/``

Configuring a demo Server
-------------------------

Demo servers must have the same ``.env`` setting as above. See the :ref:`configure-demo-servers` docs.

Local and Demo Server Testing
-----------------------------

Follow the `instructions`_ provided by the FxA team. These instructions will launch a
new Firefox instance with the necessary config already set. In the new instance of
Firefox:

#. Navigate to the page containing the Firefox Accounts form
#. If testing locally, be sure to use ``127.0.0.1`` instead of ``localhost``

Firefox Accounts iframe
-----------------------

If you need to work with/test the legacy Firefox Accounts iframe, see the :ref:`firefox-accounts-iframe` docs.

.. _instructions: https://github.com/vladikoff/fxa-dev-launcher#basic-usage-example-in-os-x
