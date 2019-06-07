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

.. _instructions: https://github.com/vladikoff/fxa-dev-launcher#basic-usage-example-in-os-x



===============================
Linking to accounts.firefox.com
===============================

The macros `fxa_link_fragment` and `fxa_cta_link` are designed to help create a valid link with all the necessary query string parameters. As well as including the `data-mozillaonline-link` attribute needed for the China repack.


Tracking Firefox Accounts referrals
-----------------------------------

When we send traffic to FxA signups, we need to send uniform parameters so measurement is straightforward.

All query string parameters need to pass the `query parameters validation
<https://mozilla.github.io/application-services/docs/accounts/metrics.html#descriptions-of-metrics-related-query-parameters>`_ applied by the FxA site as well.

Entrypoints
~~~~~~~~~~~

For the entrypoint url parameter that we generate and send to FxA servers, please use the following standard format: domain-point_of_CTA. Examples from our existing site:

```
entrypoint=mozilla.org-globalnav,
entrypoint=mozilla.org-fxa_benefits,
entrypoint=mozilla.org-firefox_new_modal,
```

We may add other entrypoints later.

If the link is part of an experiment we can indicate that the referral came from an experiment by adding the additional parameters `entrypoint_experiment` and `entrypoint_variation`

Flow
~~~~~~~~~~~~~~

For form submissions we also pass a `flow_id` and `flow_begin_time` to FxA. These are fetched from their metrics flow and inserted into the page using JavaScript. By default they are empty and it doesn't impact the flow for them to be empty.

We don't have a global function for this yet, so far it has been coded as needed for specific pages.

UTM Parameters
~~~~~~~~~~~~~~

.. Important::

    When using the `fxa_link_fragment` macro add the class `js-fxa-link-cta` to the link.

If there are not valid UTM parameters, we should add site-default utm parameters from Mozilla.org in the following format:

```
utm_content=[urlsafe content of CTA]&utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=[urlsafe category of CTA]
```

Here is an example from our current site:

```
utm_content=get-firefox-account&utm_source=www.mozilla.org&utm_medium=referral&utm_campaign=globalnav
```

If there are valid UTM parameters in the URL we should copy them onto the link to FxA.

Adding the class `js-fxa-link-cta` will trigger the global JavaScript function that handles this. If you use the `fxa_cta_link` macro to generate the link this is added automatically. If you used `fxa_link_fragment` you will need to add it manually.

DataLayer
~~~~~~~~~

For datalayer values in FxA links, please use the following standard format: `FxA-ServiceName`. Examples from our existing site:

```
data-link-type="FxA-Sync"
```

We may add other data link types later.

You can combine this with `data-link-name` to provide more information.

Do not use `data-link-type` and `data-button-name` together, GA will log two events instead of one.

