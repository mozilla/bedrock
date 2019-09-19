.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _firefox-accounts:

==========================
Firefox Accounts Referrals
==========================

Bedrock pages are often used to promote the creation of `Firefox Accounts`_ as a main *call to action* (CTA). This is typically accomplished using either a signup form, or a prominent link/button. Bedrock templates can take advantage of a series of helper macros, which can help to standardize referrals.

.. _Firefox Accounts: https://accounts.firefox.com

.. Important::

    All query string parameters passed to the macros below need to pass the `query parameters validation
    <https://mozilla.github.io/application-services/docs/accounts/metrics.html#descriptions-of-metrics-related-query-parameters>`_ applied by the Firefox Accounts server.

Signup Form
-----------

The Firefox Accounts signup form is used as a top of funnel entry point to the account creation flow. This form is shown to all browsers, but it also features some Firefox-specific logic related to signing users into `Sync`_.

.. _Sync: https://support.mozilla.org/kb/how-do-i-set-sync-my-computer

Usage
~~~~~

To use the form in a Jinja template, first import the ``fxa_email_form`` macro:

.. code-block:: jinja

    {% from "macros.html" import fxa_email_form with context %}

The form can then be invoked using:

.. code-block:: jinja

    {{ fxa_email_form(entrypoint='mozilla.org-firefox-accounts') }}

The templates's respective JavaScript and CSS bundles should also include the following dependencies:

**Javascript:**

.. code-block:: text

    js/base/mozilla-fxa-form.js
    js/base/mozilla-fxa-form-init.js

This script will automatically handle things like tracking metrics flow (see the Tracking Signups section below), as well as configuring Sync and distribution ID (e.g. the China re-pack) for Firefox browsers.

**CSS:**

.. code-block:: text

    css/base/mozilla-fxa-form.scss

This Sass file contains some useful default styling for the form.

Configuration
~~~~~~~~~~~~~

The macro provides parameters as follows (* indicates a required parameter)

+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    Parameter name    |                                                       Definition                                                           |                          Format                          |                    Example                      |
+======================+============================================================================================================================+==========================================================+=================================================+
|    entrypoint*       | Unambiguous identifier for which page of the site is the referrer.                                                         | mozilla.org-directory-page                               | 'mozilla.org-firefox-accounts'                  |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    style             | An optional parameter used to invoke an alternatively styled page at accounts.firefox.com.                                 | String                                                   |  'trailhead'                                    |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    class_name        | Applies a CSS class name to the form. Defaults to: 'fxa-email-form'                                                        | String                                                   | 'fxa-email-form'                                |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    form_title        | The main heading to be used in the form (optional with no default).                                                        | Localizable string                                       | _('Join Firefox')                               |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    intro_text        | Introductory copy to be used in the form. Defaults to a well localized string.                                             | Localizable string                                       | _('Enter your email address to get started.')   |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_text       | Button copy to be used in the form. Defaults to a well localized string.                                                   | Localizable string                                       | _('Sign Up')                                    |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_class      | CSS class names to be applied to the submit button.                                                                        | String of one or more CSS class names                    | 'mzp-c-button mzp-t-primary mzp-t-product'      |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    cta_type          | Used to indicate the type of button. Defaults to ``FxA-Monitor``                                                           | Brief keyword                                            | 'Lifecycle-Monitor'                             |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    cta_position      | Used to differentiate buttons in the event of multiples. Defaults to ``Primary``                                           | Brief keyword                                            | 'Secondary'                                     |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_campaign      | Used to identify specific marketing campaigns. Defaults to ``fxa-embedded-form``                                           | Campaign name prepended to default value                 | 'trailhead-fxa-embedded-form'                   |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_term          | Used for paid search keywords.                                                                                             | Brief keyword                                            | 'existing-users'                                |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_content       | Declared when more than one piece of content (on a page or at a URL) links to the same place, to distinguish between them. | Description of content, or name of experiment treatment  | 'get-the-rest-of-firefox'                       |
+----------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+

Invoking the macro will automatically include a set of default UTM parameters as hidden form input fields:

- ``utm_source`` is automatically assigned the value of the ``entrypoint`` parameter.
- ``utm_campaign`` is automatically set as the value of ``fxa-embedded-form``. This can be prefixed with a custom value by passing a ``utm_campaign`` value to the macro. For example, ``utm_campaign='trailhead'`` would result in a value of ``trailhead-fxa-embedded-form``.
- ``utm_medium`` is automatically set as the value of ``referral``.

Handling Distribution (aka China Repack)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The China repack of Firefox points to https://accounts.firefox.com.cn/ by default for accounts signups. To compensate for this on https://www.mozilla.org (so we don't send those visitors to the wrong place), we rely on :ref:`UITour<ui-tour>` to check the distribution ID of the browser. If the distribution ID is ``mozillaonline`` (i.e. China repack), then we replace our accounts endpoints with the alternate domain specified in the ``data-mozillaonline-link`` attribute. The logic to handle this is self contained in the macro, and in ``mozilla-fxa-form.js``.

Testing The Form
~~~~~~~~~~~~~~~~

Testing the form signup flow on a non-production environment requires some additional configuration.

**Configuring bedrock:**

Set the following in your local ``.env`` file:

.. code-block:: text

    FXA_ENDPOINT=https://latest.dev.lcip.org/

**Configuring a demo Server:**

Demo servers must have the same ``.env`` setting as above. See the :ref:`configure-demo-servers` docs.

**Local and demo server testing:**

Follow the `instructions`_ provided by the FxA team. These instructions will launch a
new Firefox instance with the necessary config already set. In the new instance of
Firefox:

#. Navigate to the page containing the Firefox Accounts form
#. If testing locally, be sure to use ``127.0.0.1`` instead of ``localhost``

.. _instructions: https://github.com/vladikoff/fxa-dev-launcher#basic-usage-example-in-os-x


Linking to accounts.firefox.com
-------------------------------

The ``fxa_cta_link`` macro is designed to help create a valid *call to action* (CTA) link to https://accounts.firefox.com, with all the necessary query string parameters. This macro will also generate a valid ``data-mozillaonline-link`` attribute needed for the China repack distribution.

Usage
~~~~~

To use the link in a Jinja template, first import the `fxa_cta_link` macro:

.. code-block:: jinja

    {% from "macros.html" import fxa_cta_link with context %}

A link can then be invoked using:

.. code-block:: jinja

    {{ fxa_cta_link(
        entrypoint='mozilla.org-firefox-accounts',
        button_text=_('Create a Firefox Account')
    }}

Configuration
~~~~~~~~~~~~~

The macro provides parameters as follows (* indicates a required parameter)

+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    Parameter name    |                                                       Definition                                                       |                          Format                          |                    Example                      |
+======================+========================================================================================================================+==========================================================+=================================================+
|    entrypoint*       | Unambiguous identifier for which page of the site is the referrer.                                                     | 'mozilla.org-directory-page'                             | 'mozilla.org-firefox-accounts'                  |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    service_type      | The type of service the referral will initiate. Defaults to: 'sync'.                                                   | String                                                   | 'sync'                                          |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    action            | The type of action the link will perform. Defaults to 'signin'.                                                        | String                                                   | 'signup'                                        |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_text*      | The button copy to be used in the call to action.                                                                      | Localizable string                                       | _('Create a Firefox Account')                   |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    account_id        | An HTML 'id' to be added to the link.                                                                                  | String                                                   | 'account-hero-button'                           |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_class      | A CSS class names to be applied to the link.                                                                           | String of one or more CSS class names                    | 'mzp-c-button mzp-t-primary mzp-t-product'      |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_campaign*     | Used to identify specific marketing campaigns. Should have default value which is descriptive of the page element.     | Campaign name appended to default value                  | 'accounts-page-hero'                            |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_term          | Used for paid search keywords.                                                                                         | Brief keyword                                            | 'existing-users'                                |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_content       | It should only be declared when there is more than one piece of content on a page linking to the same place.           | Description of content, or name of experiment treatment  | 'get-the-rest-of-firefox'                       |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+

Invoking the macro will automatically include a set of default UTM parameters as query string values:

- ``utm_source`` is automatically assigned the value of the ``entrypoint`` parameter.
- ``utm_medium`` is automatically set as the value of ``referral``.

.. Note::

    There is also a ``fxa_link_fragment`` macro which will construct only valid ``href`` and ``data-mozillaonline-link`` properties. This is useful when constructing an inline link inside a paragraph, for example. The ``fxa_link_fragment`` will accept the same ``entrypoint``, ``service_type``, ``action`` and ``utm_*`` values as the ``fxa_cta_link`` macro.


Linking to monitor.firefox.com
-------------------------------

The ``monitor_button`` macro is designed to help create a valid *call to action* (CTA) link to https://monitor.firefox.com.

Usage
~~~~~

To use the button in a Jinja template, first import the `monitor_button` macro:

.. code-block:: jinja

    {% from "macros.html" import monitor_button with context %}

A button can then be invoked using:

.. code-block:: jinja

    {{ monitor_button(entrypoint='mozilla.org-firefox-accounts')}}

The templates's respective JavaScript bundle should also include the following dependencies:

.. code-block:: text

    js/base/mozilla-monitor-button.js
    js/base/mozilla-monitor-button-init.js

This script will automatically handle things like tracking metrics flow (in the same way we do for https://accounts.firefox.com).

Configuration
~~~~~~~~~~~~~

The macro provides parameters as follows (* indicates a required parameter)

+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    Parameter name    |                                                       Definition                                                       |                          Format                          |                    Example                      |
+======================+========================================================================================================================+==========================================================+=================================================+
|    entrypoint*       | Unambiguous identifier for which page of the site is the referrer.                                                     | 'mozilla.org-directory-page'                             | 'mozilla.org-firefox-accounts'                  |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    form_type         | The type of form to display. Defaults to: 'button'.                                                                    | String                                                   | 'email'                                         |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_text       | The button copy to be used in the call to action.  Default to a well localized string.                                 | Localizable string                                       | _('Sign In to Monitor')                         |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_class      | A class name to be applied to the link (typically for styling with CSS).                                               | String of one or more class names                        | 'mzp-c-button mzp-t-primary mzp-t-product'      |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_id         | A unique ID to apply to the link, for cases where multiple buttons appear on the same page.                            | String                                                   | 'fxa-monitor-submit'                            |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_campaign*     | Used to identify specific marketing campaigns. Should have default value which is descriptive of the page component.   | Campaign name appended to default value                  | 'accounts-page-hero'                            |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_term          | Used for paid search keywords.                                                                                         | Brief keyword                                            | 'existing-users'                                |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_content       | It should only be declared when there is more than one piece of content on a page linking to the same place.           | Description of content, or name of experiment treatment  | 'get-the-rest-of-firefox'                       |
+----------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+

Invoking the macro will automatically include a set of default UTM parameters as query string values:

- ``utm_source`` is automatically assigned the value of the ``entrypoint`` parameter.
- ``utm_medium`` is automatically set as the value of ``referral``.


Tracking Sign-ups / Sign-ins
----------------------------

For both Firefox Accounts form submissions and Firefox Monitor referrals, we also pass ``device_id``, ``flow_id`` and ``flow_begin_time`` parameters to track top-of-funnel metrics. These are values fetched from a metrics flow API endpoint, and are instered back into the form / link along with the other standard referral parameters. This functionality is handled by ``mozilla-fxa-form.js`` and ``mozilla-monitor-button.js`` respectively.

.. Important::

    Requests to metrics API endpoints should only be made when an associated CTA is visibly displayed on a page. For example, if a page contains both a Firefox Accounts signup form and a Firefox Monitor button, but only one CTA is displayed at any one time, then only the metrics request associated with that CTA should occur.


Tracking External Referrers
---------------------------

If the URL of a bedrock page contains existing UTM parameters on page load, bedrock will attempt to automatically use those values to replace the inline UTM parameters in Firefox Accounts links. This is handled using a client side script in the site common bundle which can be found in ``/media/js/base/fxa-utm-referral.js``.

The behavior is as follows:

- UTM paramters will only be replaced if the page URL contains both a valid ``utm_source`` and ``utm_campaign`` parameter. All other UTM parameters are considered optional, but will still be passed as long as the required parameters exist.
- If the above criteria is satisfied, then UTM parameters on FxA links will be replaced in their entirety with the UTM parameters from the page URL. This is to avoid mixing referral data from different campaigns.

.. Important::

    Links generated by the ``fxa_email_form`` and ``fxa_cta_link`` will automatically be covered by this script. For links generated using the ``fxa_link_fragment`` macro, you will need to manually add a CSS class of ``js-fxa-cta-link`` to trigger the function. This script does not yet cover the monitor button or signup form macro.


Google Analytics Guidelines
---------------------------

For GTM datalayer attribute values in FxA links, please use the :ref:`analytics<analytics>` documentation.
