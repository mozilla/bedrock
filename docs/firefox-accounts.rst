.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _firefox-accounts:

==========================
Firefox Accounts Referrals
==========================

Marketing pages often promote the creation of a `Firefox Account`_ (FxA) as a common *call to action*
(CTA). This is typically accomplished using either a signup form, or a prominent link/button. Other
products such as `Mozilla VPN`_ use similar Firefox Account auth flows to manage subscriptions. To
accomplish these tasks, bedrock templates can take advantage of a series of Python helpers which can
be used to standardize product referrals, and make supporting these auth flows easier.

.. Note::

    The helpers below can typically be shown to all browsers, but some also feature logic specific
    to desktop Firefox, such as signing users into `Sync`_.

.. _Firefox Account: https://accounts.firefox.com
.. _Mozilla VPN: https://www.mozilla.org/products/vpn/
.. _Sync: https://support.mozilla.org/kb/how-do-i-set-sync-my-computer


Firefox Account Signup Form
---------------------------

Use the ``fxa_email_form`` macro to display a Firefox Account signup form on a page.

Usage
~~~~~

To use the form in a Jinja template, first import the ``fxa_email_form`` macro:

.. code-block:: jinja

    {% from "macros.html" import fxa_email_form with context %}

The form can then be invoked using:

.. code-block:: jinja

    {{ fxa_email_form(entrypoint='mozilla.org-firefox-accounts') }}

The template's respective JavaScript and CSS bundles should also include the following dependencies:

**Javascript:**

.. code-block:: text

    js/base/mozilla-fxa-form.js
    js/base/mozilla-fxa-form-init.js

**CSS:**

.. code-block:: css

    @import '../path/to/fxa-form';

The JavaScript files will automatically handle things adding metrics parameters, as well as
configuring Sync and distribution ID (e.g. the China re-pack) for Firefox desktop browsers (more
info on these further down the page). The CSS file contains some default styling for the signup form.

Configuration
~~~~~~~~~~~~~

The signup form macro accepts the following parameters (* indicates a required parameter)

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
|    form_title              | The main heading to be used in the form (optional with no default).                                                        | Localizable string                                       | _('Join Firefox')                               |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    intro_text              | Introductory copy to be used in the form. Defaults to a well localized string.                                             | Localizable string                                       | _('Enter your email address to get started.')   |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_text             | Button copy to be used in the form. Defaults to a well localized string.                                                   | Localizable string                                       | _('Sign Up')                                    |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    button_class            | CSS class names to be applied to the submit button.                                                                        | String of one or more CSS class names                    | 'mzp-c-button mzp-t-primary mzp-t-product'      |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_campaign            | Used to identify specific marketing campaigns. Defaults to ``fxa-embedded-form``                                           | Campaign name prepended to default value                 | 'trailhead-fxa-embedded-form'                   |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_term                | Used for paid search keywords.                                                                                             | Brief keyword                                            | 'existing-users'                                |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+
|    utm_content             | Declared when more than one piece of content (on a page or at a URL) links to the same place, to distinguish between them. | Description of content, or name of experiment treatment  | 'get-the-rest-of-firefox'                       |
+----------------------------+----------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+-------------------------------------------------+

Invoking the macro will automatically include a set of default UTM parameters as hidden form input fields:

- ``utm_source`` is automatically assigned the value of the ``entrypoint`` parameter.
- ``utm_campaign`` is automatically set as the value of ``fxa-embedded-form``. This can be prefixed with a custom value by passing a ``utm_campaign`` value to the macro. For example, ``utm_campaign='trailhead'`` would result in a value of ``trailhead-fxa-embedded-form``.
- ``utm_medium`` is automatically set as the value of ``referral``.


Firefox Account Links
---------------------

Use the ``fxa_button`` helper to create a CTA button or link to https://accounts.firefox.com/.

Usage
~~~~~

.. code-block:: jinja

    {{ fxa_button(entrypoint='mozilla.org-firefox-accounts', button_text='Sign In') }}

.. Note::

    There is also a ``fxa_link_fragment`` helper which will construct only valid ``href``
    and ``data-mozillaonline-link`` properties. This is useful when constructing an
    inline link inside a paragraph, for example.

For more information on the available parameters, read the "Common FxA Parameters"
section further below.


Firefox Monitor Links
---------------------

Use the ``monitor_fxa_button`` helper to link to https://monitor.firefox.com/ via a
Firefox Accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ monitor_fxa_button(entrypoint=_entrypoint, button_text='Sign Up for Monitor') }}

For more information on the available parameters, read the "Common FxA Parameters"
section further below.


Pocket Links
------------

Use the ``pocket_fxa_button`` helper to link to https://getpocket.com/ via a
Firefox Accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ pocket_fxa_button(entrypoint='mozilla.org-firefox-pocket', button_text='Try Pocket Now', optional_parameters={'s': 'ffpocket'}) }}

For more information on the available parameters, read the "Common FxA Parameters"
section below.


Common FxA Parameters
---------------------

The ``fxa_button``, ``pocket_fxa_button``, and ``monitor_fxa_button`` helpers
all support the same standard parameters:

+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    Parameter name          |                                                       Definition                                                       |                          Format                          |                                                Example                                                 |
+============================+========================================================================================================================+==========================================================+========================================================================================================+
|    entrypoint*             | Unambiguous identifier for which page of the site is the referrer. This also serves as a value for 'utm_source'.       | 'mozilla.org-firefox-pocket'                             | 'mozilla.org-firefox-pocket'                                                                           |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    button_text*            | The button copy to be used in the call to action.                                                                      | Localizable string                                       | 'Try Pocket Now'                                                                                       |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    class_name              | A class name to be applied to the link (typically for styling with CSS).                                               | String of one or more class names                        | 'pocket-main-cta-button'                                                                               |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    is_button_class         | A boolean value that dictates if the CTA should be styled as a button or a link. Defaults to 'True'.                   | Boolean                                                  | True or False                                                                                          |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    include_metrics         | A boolean value that dictates if metrics parameters should be added to the button href. Defaults to 'True'.            | Boolean                                                  | True or False                                                                                          |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optional_parameters     | An dictionary of key value pairs containing additional parameters to append the the href.                              | Dictionary                                               | {'s': 'ffpocket'}                                                                                      |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optiona_attributes      | An dictionary of key value pairs containing additional data attributes to include in the button.                       | Dictionary                                               | {'data-cta-text': 'Try Pocket Now', 'data-cta-type': 'activate pocket','data-cta-position': 'primary'} |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

.. Note::

    The ``fxa_button`` helper also supports an additional ``action`` parameter,
    which accepts the values ``signup``, ``signin``, and ``email`` for
    configuring the type of authentication flow.


Mozilla VPN Links
-----------------

Use the ``vpn_sign_in_link`` helper to create a sign-in link to https://vpn.mozilla.org/ via a
Firefox Accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ vpn_sign_in_link(entrypoint='www.mozilla.org-vpn-product-page', link_text='Sign In') }}

Use the ``vpn_subscribe_link`` helpers to create a VPN subscription link via a
Firefox Accounts auth flow.

Usage
~~~~~

.. code-block:: jinja

    {{ vpn_subscribe_link(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN') }}

Common VPN Parameters
~~~~~~~~~~~~~~~~~~~~~

Both helpers for Mozilla VPN support the same parameters (* indicates a required parameter)

+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    Parameter name          |                                                       Definition                                                       |                          Format                          |                                                Example                                                 |
+============================+========================================================================================================================+==========================================================+========================================================================================================+
|    entrypoint*             | Unambiguous identifier for which page of the site is the referrer. This also serves as a value for 'utm_source'.       | 'www.mozilla.org-page-name'                              | 'www.mozilla.org-vpn-product-page'                                                                     |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    link_text*              | The link copy to be used in the call to action.                                                                        | Localizable string                                       | 'Get Mozilla VPN'                                                                                      |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    class_name              | A class name to be applied to the link (typically for styling with CSS).                                               | String of one or more class names                        | 'vpn-button'                                                                                           |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    lang                    | Page locale code. Used to query the right subscription plan ID in conjunction to country code.                         | Locale string                                            | 'de'                                                                                                   |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    country_code            | Country code provided by the CDN. Used to determine the appropriate subscription plan ID.                              | Two digit, uppercase country code                        | 'DE'                                                                                                   |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optional_parameters     | An dictionary of key value pairs containing additional parameters to append the the href.                              | Dictionary                                               | {'utm_campaign': 'vpn-product-page'}                                                                   |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optiona_attributes      | An dictionary of key value pairs containing additional data attributes to include in the button.                       | Dictionary                                               | {'data-cta-text': 'VPN Sign In', 'data-cta-type': 'fxa-vpn', 'data-cta-position': 'navigation'}        |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

The ``vpn_subscribe_link`` helper has an additional ``plan`` parameter to support linking to different subscription plans.

+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    Parameter name          |                                                       Definition                                                       |                          Format                          |                                                Example                                                 |
+============================+========================================================================================================================+==========================================================+========================================================================================================+
|    plan                    | Subscription plan ID. Defaults to 12-month plan.                                                                       | '12-month'                                               | '12-month', '6-month', or 'monthly'                                                                    |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

Tracking Same-Site Links for Mozilla VPN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often we promote Mozilla VPN on different pages via the use of same-site referral
links to the product landing page. For example, we display a "Get Mozilla VPN"
button in the main navigation that links to the ``/products/vpn/`` landing page.

In scenarios such as this we want to understand how many people click the link in the
navigation and go on to signup / subscribe to VPN. To achieve this, we have some
additional logic in ``fxa-utm-referral.js`` that will check for a specific cookie
that gets set when someone clicks a specific referral link.

To create a Mozilla VPN referral link, you can use the ``vpn_product_referral_link`` helper:

.. code-block:: jinja

    {{ vpn_product_referral_link(
        referral_id='navigation',
        link_text='Get Mozilla VPN',
        class_name='mzp-t-secondary mzp-t-md',
        page_anchor='#pricing',
        optional_attributes= {
            'data-cta-text' : 'Get Mozilla VPN',
            'data-cta-type' : 'button',
            'data-cta-position' : 'navigation',
        }
    ) }}

The helper supports the following parameters:

+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    Parameter name          |                                                       Definition                                                       |                          Format                          |                                                Example                                                 |
+============================+========================================================================================================================+==========================================================+========================================================================================================+
|    referral_id*            | The ID for the referring page / component. This serves as a value for 'utm_campaign'.                                  | String                                                   | 'navigation'                                                                                           |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    link_text*              | The link copy to be used in the call to action.                                                                        | Localizable string                                       | 'Get Mozilla VPN'                                                                                      |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    class_name              | A class name to be applied to the link (typically for styling with CSS).                                               | String of one or more class names                        | 'mzp-t-secondary mzp-t-md'                                                                             |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    page_anchor             | An optional page anchor for the link destination.                                                                      | String                                                   | '#pricing'                                                                                             |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+
|    optiona_attributes      | An dictionary of key value pairs containing additional data attributes to include in the button.                       | Dictionary                                               | {'data-cta-text': 'Get Mozilla VPN', 'data-cta-type': 'button', 'data-cta-position': 'navigation'}     |
+----------------------------+------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------+--------------------------------------------------------------------------------------------------------+

When someone clicks the link a cookie gets set with a 1 hour expiry. The
``fxa-utm-referral.js`` script will then check for the existence of this
cookie on page load and update the product landing page subscription links
with utm parameters that attribute where the click came from.

For example, a referral cookie with the ID ``navigation`` would result
in the following utm parameters being set:

  - ``utm_source=www.mozilla.org``.
  - ``utm_campaign=navigation``.
  - ``utm_medium=referral``.

.. Note::

    The above attribution will only be applied if there are not already
    utm parameters on the product landing page URL. We will also respect
    privacy and only set the cookie if DNT is disabled.


Link Metrics
------------

When using any of the FxA or VPN helpers that link directly to FxA,
a templates's respective JavaScript bundle should also include the following
dependencies:

.. code-block:: text

    js/base/mozilla-fxa-product-button.js
    js/base/mozilla-fxa-product-button-init.js

This script automatically adds metrics parameters to the button ``href``:

- ``deviceId``
- ``flowId``
- ``flowBeginTime``

These are values are fetched from an API endpoint, and are instered back into
the destination link along with the other standard referral parameters.

.. Important::

    Requests to metrics API endpoints should only be made when an associated CTA is
    visibly displayed on a page. For example, if a page contains both a Firefox Accounts
    signup form and a Firefox Monitor button, but only one CTA is displayed at any one
    time, then only the metrics request associated with that CTA should occur. For links
    generated using the ``fxa_link_fragment`` helper, you will also need to manually
    add a CSS class of ``js-fxa-product-button`` to trigger the script.


Tracking External Referrers
---------------------------

If the URL of a bedrock page contains existing UTM parameters on page load, bedrock will
attempt to automatically use those values to replace the inline UTM parameters in
Firefox Account and Mozilla VPN links. This is handled using a client side script in the
site common bundle which can be found in ``/media/js/base/fxa-utm-referral.js``.

The behavior is as follows:

- UTM paramters will only be replaced if the page URL contains both a valid ``utm_source`` and ``utm_campaign`` parameter. All other UTM parameters are considered optional, but will still be passed as long as the required parameters exist.
- If the above criteria is satisfied, then UTM parameters on FxA links will be replaced in their entirety with the UTM parameters from the page URL. This is to avoid mixing referral data from different campaigns.

.. Important::

    Links generated by the FxA button helpers will automatically be covered by this
    script. For links generated using the ``fxa_link_fragment`` helper, you will
    need to manually add a CSS class of ``js-fxa-cta-link`` to trigger the behavior.


URL Parameter Conventions
-------------------------

When choosing URL parameter values, the following conventions help to support uniformity in code and
predictability in retroactive analysis.

* Use lower case characters in parameter values.
* Separate words in parameter values with hyphens.
* Follow parameter naming patterns established in previous iterations of a page.


Firefox Sync and UITour
-----------------------

Since Firefox 80 the FxA link and email form macros use :ref:`UITour<ui-tour>` to show the Firefox Accounts page
and log the browser into Sync or an Account. For non-Firefox browsers or if UITour is not available, the flow uses
normal links that allow users to log into FxA as a website only without connecting the Firefox Desktop client.
This UITour flow allows the Firefox browser to determine the correct FxA server and authentication flow.
This transition was introduced to later migrate Firefox Desktop to an OAuth based client authentication flow.

The script that handles this logic is ``/media/js/base/mozilla-fxa-link.js``, and will automatically apply
to any link with a ``js-fxa-cta-link`` class name. The current code automatically detects if you are in the
supported browser for this flow and updates links to drive them through the UITour API. The UITour
``showFirefoxAccounts`` action supports flow id parameters, UTM parameters and the email data field.

We hope to remove the legacy non-UITour login logic after 1 or 2 ESRs.


Handling Distribution (aka China Repack)
----------------------------------------

The China repack of Firefox points to https://accounts.firefox.com.cn/ by default for
FxA accounts signups. To compensate for this on https://www.mozilla.org (so we don't send
those visitors to the wrong place), we rely on :ref:`UITour<ui-tour>` to check the
distribution ID of the browser. If the distribution ID is ``mozillaonline``
(i.e. China repack), then we replace our accounts endpoints with the alternate domain
specified in the ``data-mozillaonline-link`` attribute. The logic to handle this is
self contained in the associated helper scripts and handled automatically.

.. Note::

    This logic does not apply to Mozilla VPN, since the product is not available
    in China.


Testing Signup Flows
--------------------

Testing the Firefox Account signup flows on a non-production environment requires
some additional configuration.

**Configuring bedrock:**

Set the following in your local ``.env`` file:

.. code-block:: text

    FXA_ENDPOINT=https://stable.dev.lcip.org/

For Mozilla VPN links you can also set:

.. code-block:: text

    VPN_ENDPOINT=https://stage-vpn.guardian.nonprod.cloudops.mozgcp.net/
    VPN_SUBSCRIPTION_URL=https://accounts.stage.mozaws.net/

.. Note::

    The above values for staging are already set by default when ``Dev=True``,
    which will also apply to demo servers. You may only need to configure
    your ``.env`` file if you wish to change a setting to something else.

**Local and demo server testing:**

Follow the `instructions`_ provided by the FxA team. These instructions will launch a
new Firefox instance with the necessary config already set. In the new instance of
Firefox:

#. Navigate to the page containing the Firefox Accounts CTA.
#. If testing locally, be sure to use ``127.0.0.1`` instead of ``localhost``

.. _instructions: https://github.com/vladikoff/fxa-dev-launcher#basic-usage-example-in-os-x


Google Analytics Guidelines
---------------------------

For GTM datalayer attribute values in FxA links, please use the :ref:`analytics<analytics>` documentation.
