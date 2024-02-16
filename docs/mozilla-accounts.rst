.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _mozilla-accounts-helpers:

========================
Mozilla accounts helpers
========================

.. Note::

    Since a rebranding in October 2023, we now refer to "Mozilla accounts" in our web pages instead
    of "Firefox accounts". This rebranding is so far superficial, and sign up flows still go to
    ``accounts.firefox.com``. Because of this, our internal code and helpers still use ``FxA`` or
    ``fxa`` as a common abbreviation. However the language used around them should now be
    "Mozilla accounts" going forward.

Marketing pages often promote the creation of a `Mozilla account`_ as a common *call to action*
(CTA). This is typically accomplished using either a sign-up form, or a prominent link/button. Other
products such as `Mozilla VPN`_ use similar account auth flows to manage subscriptions. To accomplish
these tasks, bedrock templates can take advantage of a series of Python helpers which can be used to
standardize product referrals, and make supporting these auth flows easier.

.. Note::

    See the attribution docs (:ref:`mozilla-accounts-attribution`) for more a detailed description of
    the analytics functions these helpers provide.

Mozilla account sign-up form
----------------------------

Use the ``fxa_email_form`` macro to display a Mozilla account sign-up form on a page.

Usage
~~~~~

To use the form in a Jinja template, first import the ``fxa_email_form`` macro:

.. code-block:: jinja

    {% from "macros.html" import fxa_email_form with context %}

The form can then be invoked using:

.. code-block:: jinja

    {{ fxa_email_form(entrypoint='mozilla.org-firefox-accounts') }}

The macro's respective JavaScript and CSS dependencies should also be
imported in the page:

**Javascript:**

.. code-block:: javascript

    import FxaForm from './path/to/fxa-form.es6.js';

    FxaForm.init();

The above JS is also available as a pre-compiled bundle, which can be included
directly in a template:

.. code-block:: jinja

    {{ js_bundle('fxa_form') }}

**CSS:**

.. code-block:: css

    @import '../path/to/fxa-form';

The JavaScript files will automatically handle things such as adding metrics parameters
for Firefox desktop browsers. The CSS file contains some default styling for the sign-up form.

Configuration
~~~~~~~~~~~~~

The sign-up form macro accepts the following parameters (* indicates a required parameter)

+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    Parameter name          |                                                       Definition                                                           |                          Format                          |                    Example                      |
+============================+============================================================================================================================+==========================================================+=================================================+
|    entrypoint*             | Unambiguous identifier for which page of the site is the referrer.                                                         | mozilla.org-directory-page                               | 'mozilla.org-firefox-accounts'                  |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    entrypoint_experiment   | Used to identify experiments.                                                                                              | Experiment ID                                            | 'whatsnew-headlines'                            |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    entrypoint_variation    | Used to track page variations in multivariate tests. Usually just a number or letter but could be a short keyword.         | Variant identifier                                       | 'b'                                             |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    style                   | An optional parameter used to invoke an alternatively styled page at accounts.firefox.com.                                 | String                                                   |  'trailhead'                                    |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    class_name              | Applies a CSS class name to the form. Defaults to: 'fxa-email-form'                                                        | String                                                   | 'fxa-email-form'                                |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    form_title              | The main heading to be used in the form (optional with no default).                                                        | Localizable string                                       | 'Join Firefox' .                                |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    intro_text              | Introductory copy to be used in the form. Defaults to a well localized string.                                             | Localizable string                                       | 'Enter your email address to get started.' .    |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_text             | Button copy to be used in the form. Defaults to a well localized string.                                                   | Localizable string                                       | 'Sign Up' .                                     |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_class            | CSS class names to be applied to the submit button.                                                                        | String of one or more CSS class names                    | 'mzp-c-button mzp-t-primary mzp-t-product'      |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_campaign            | Used to identify specific marketing campaigns. Defaults to ``fxa-embedded-form``                                           | Campaign name prepended to default value                 | 'trailhead-fxa-embedded-form'                   |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_term                | Used for paid search keywords.                                                                                             | Brief keyword                                            | 'existing-users'                                |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_content             | Declared when more than one piece of content (on a page or at a URL) links to the same place, to distinguish between them. | Description of content, or name of experiment treatment  | 'get-the-rest-of-firefox'                       |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+

Invoking the macro will automatically include a set of default :abbr:`UTM (Urchin Tracking Module)` parameters as hidden form input fields:

- ``utm_source`` is automatically assigned the value of the ``entrypoint`` parameter.
- ``utm_campaign`` is automatically set as the value of ``fxa-embedded-form``. This can be prefixed with a custom value by passing a ``utm_campaign`` value to the macro. For example, ``utm_campaign='trailhead'`` would result in a value of ``trailhead-fxa-embedded-form``.
- ``utm_medium`` is automatically set as the value of ``referral``.

.. Note::

    When signing into a Mozilla account using this form on a Firefox Desktop browser, it will also
    activate the `Sync`_ feature.


Mozilla account links
---------------------

Use the ``fxa_button`` helper to create a :abbr:`CTA (Call To Action)` button or link to https://accounts.firefox.com/.

Usage
~~~~~

.. code-block:: jinja

    {{ fxa_button(entrypoint='mozilla.org-firefox-sync-page', button_text='Sign In') }}

.. Note::

    There is also a ``fxa_link_fragment`` helper which will construct a valid ``href``
    property. This is useful when constructing an inline link inside a paragraph, for example.

.. Note::

    When signing into a Mozilla account using this link on a Firefox Desktop browser, it will also
    activate the `Sync`_ feature.

For more information on the available parameters, read the "Common Parameters"
section further below.


Mozilla Monitor links
---------------------

Use the ``monitor_fxa_button`` helper to link to https://monitor.mozilla.org/ via a
Mozilla accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ monitor_fxa_button(entrypoint=_entrypoint, button_text='Sign Up for Monitor') }}

For more information on the available parameters, read the "Common Parameters"
section further below.


Pocket links
------------

Use the ``pocket_fxa_button`` helper to link to https://getpocket.com/ via a
Mozilla accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ pocket_fxa_button(entrypoint='mozilla.org-firefox-pocket', button_text='Try Pocket Now', optional_parameters={'s': 'ffpocket'}) }}

For more information on the available parameters, read the "Common Parameters"
section below.


Common Parameters
-----------------

The ``fxa_button``, ``pocket_fxa_button``, and ``monitor_fxa_button`` helpers
all support the same standard parameters:

+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| Parameter name      | Definition                                                                                                                    | Format                            | Example                                                                                                |
+=====================+===============================================================================================================================+===================================+========================================================================================================+
| entrypoint*         | Unambiguous identifier for which page of the site is the referrer. This also serves as a value for 'utm_source'.              | 'mozilla.org-firefox-pocket'      | 'mozilla.org-firefox-pocket'                                                                           |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| button_text*        | The button copy to be used in the call to action.                                                                             | Localizable string                | 'Try Pocket Now'                                                                                       |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| class_name          | A class name to be applied to the link (typically for styling with CSS).                                                      | String of one or more class names | 'pocket-main-cta-button'                                                                               |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| is_button_class     | A boolean value that dictates if the :abbr:`CTA (Call To Action)` should be styled as a button or a link. Defaults to 'True'. | Boolean                           | True or False                                                                                          |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| include_metrics     | A boolean value that dictates if metrics parameters should be added to the button href. Defaults to 'True'.                   | Boolean                           | True or False                                                                                          |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| optional_parameters | An dictionary of key value pairs containing additional parameters to append the the href.                                     | Dictionary                        | {'s': 'ffpocket'}                                                                                      |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+
| optional_attributes | An dictionary of key value pairs containing additional data attributes to include in the button.                              | Dictionary                        | {'data-cta-text': 'Try Pocket Now', 'data-cta-type': 'activate pocket','data-cta-position': 'primary'} |
+---------------------+-------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------------------------------------------------------------------------------------------------------+

.. Note::

    The ``fxa_button`` helper also supports an additional ``action`` parameter,
    which accepts the values ``signup``, ``signin``, and ``email`` for
    configuring the type of authentication flow.

.. _vpn-helpers:

Mozilla :abbr:`VPN (Virtual Private Network)` Links
---------------------------------------------------

Use the ``vpn_subscribe_link`` helpers to create a :abbr:`VPN (Virtual Private Network)` subscription link via a
Mozilla accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ vpn_subscribe_link(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN') }}

Common :abbr:`VPN (Virtual Private Network)` Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Both helpers for Mozilla :abbr:`VPN (Virtual Private Network)` support the same parameters (* indicates a required parameter)

+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    Parameter name          |                                                       Definition                                                             |                Format                |                                                Example                                                 |
+============================+==============================================================================================================================+======================================+========================================================================================================+
|    entrypoint*             | Unambiguous identifier for which page of the site is the referrer. This also serves as a value for 'utm_source'.             | 'www.mozilla.org-page-name'          | 'www.mozilla.org-vpn-product-page'                                                                     |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    link_text*              | The link copy to be used in the call to action.                                                                              | Localizable string                   | 'Get Mozilla VPN'                                                                                      |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    class_name              | A class name to be applied to the link (typically for styling with CSS).                                                     | String of one or more class names    | 'vpn-button'                                                                                           |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    lang                    | Page locale code. Used to query the right subscription plan ID in conjunction to country code.                               | Locale string                        | 'de'                                                                                                   |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    country_code            | Country code provided by the :abbr:`CDN (Content Delivery Network)`. Used to determine the appropriate subscription plan ID. | Two digit, uppercase country code    | 'DE'                                                                                                   |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    bundle_relay            | Generate a link that will bundle both Mozilla VPN and Firefox Relay in a single subscription. Defaults to False.             | Boolean                              | True, False                                                                                            |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optional_parameters     | An dictionary of key value pairs containing additional parameters to append the the href.                                    | Dictionary                           | {'utm_campaign': 'vpn-product-page'}                                                                   |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optional_attributes     | An dictionary of key value pairs containing additional data attributes to include in the button.                             | Dictionary                           | {'data-cta-text': 'VPN Sign In', 'data-cta-type': 'fxa-vpn', 'data-cta-position': 'navigation'}        |
+----------------------------+------------------------------------------------------------------------------------------------------------------------------+--------------------------------------+--------------------------------------------------------------------------------------------------------+

The ``vpn_subscribe_link`` helper has an additional ``plan`` parameter to support linking to different subscription plans.

+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    Parameter name          |                                                       Definition                                                       |                          Format                          |                                                Example                                                 |
+============================+========================================================================================================================+==========================================================+========================================================================================================+
|    plan                    | Subscription plan ID. Defaults to 12-month plan.                                                                       | '12-month'                                               | '12-month' or 'monthly'                                                                                |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

Firefox Sync and UITour
-----------------------

Since Firefox 80 the accounts link and email form macros use :ref:`UITour<ui-tour>` to show the
Mozilla accounts page and log the browser into Sync or an account. For non-Firefox browsers or if
UITour is not available, the flow uses normal links that allow users to log into the Mozilla accounts
website only, without connecting the Firefox Desktop client. This UITour flow allows the Firefox browser
to determine the correct Mozilla accounts server and authentication flow (this includes handling the
China Repack build of Firefox). This transition was introduced to later migrate Firefox Desktop to an
OAuth based client authentication flow.

The script that handles this logic is ``/media/js/base/fxa-link.js``, and will automatically apply
to any link with a ``js-fxa-cta-link`` class name. The current code automatically detects if you are in the
supported browser for this flow and updates links to drive them through the UITour API. The UITour
``showFirefoxAccounts`` action supports flow id parameters, :abbr:`UTM (Urchin Tracking Module)` parameters
and the email data field.


Testing Sign-up Flows
---------------------

Testing the Mozilla account sign-up flows on a non-production environment requires
some additional configuration.

**Configuring bedrock:**

Set the following in your local ``.env`` file:

.. code-block:: text

    FXA_ENDPOINT=https://accounts.stage.mozaws.net/

For Mozilla :abbr:`VPN (Virtual Private Network)` links you can also set:

.. code-block:: text

    VPN_ENDPOINT=https://stage.guardian.nonprod.cloudops.mozgcp.net/
    VPN_SUBSCRIPTION_URL=https://accounts.stage.mozaws.net/

.. Note::

    The above values for staging are already set by default when ``Dev=True``,
    which will also apply to demo servers. You may only need to configure
    your ``.env`` file if you wish to change a setting to something else.

.. _Mozilla account: https://accounts.firefox.com
.. _Mozilla VPN: https://www.mozilla.org/products/vpn/
.. _Sync: https://support.mozilla.org/kb/how-do-i-set-sync-my-computer
