.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _sendtodevice:

=====================
Send to Device Widget
=====================

The *Send to Device* widget is a single macro form which facilitates the sending of a download link from a desktop browser to a mobile device. The form allows sending via SMS or email, although the SMS copy & messaging is shown only to those in the configured countries. Geo-location is handled in JavaScript using a `bedrock view <https://github.com/mozilla/bedrock/blob/7ae0f693ab0347057b56397462351f7085205e3c/bedrock/base/views.py#L31>`_ that gets the request country from `CloudFlare CDN headers <https://support.cloudflare.com/hc/en-us/articles/200168236-What-does-CloudFlare-IP-Geolocation-do->`_. For users without JavaScript, the widget falls back to a standard email form.

.. important:: This widget should only be shown to a limited set of locales who are set up to receive the emails. For those locales not in the list, direct links to the respective app stores should be shown instead. If a user is on iOS or Android, CTA buttons should also link directly to respective app stores instead of showing the widget. This logic should be handled on a page-by-page basis to cover individual needs.

.. note:: A full list of supported locales can be found in ``settings/base.py`` under ``SEND_TO_DEVICE_LOCALES``, which can be used in the template logic for each page to show the form. The countries enabled for SMS for each message are defined in the `running configuration <https://mozmeao.github.io/www-config/configs/>`_ per the environment names in ``SEND_TO_DEVICE_MESSAGE_SETS`` in the settings file.

Usage
-----

1. Include this macro::

    {% from "macros.html" import send_to_device with context %}

2. Add the appropriate lang file to the page template::

    {% add_lang_files "firefox/sendto" %}

3. Make sure necessary files are in your CSS/JS bundles:

  - ``'css/protocol/components/send-to-device.scss'``

  - ``'js/base/send-to-device.js'``

4. Include the macro in your page template::

    {{ send_to_device() }}

5. Initialize the widget:

  In your page JS, initialize the widget using::

    var form = new Mozilla.SendToDevice();
    form.init();

  By default the ``init()`` function will look for a form with an HTML id of ``send-to-device``. If you need to pass another id, you can do so directly::

    var form = new Mozilla.SendToDevice('my-custom-form-id');
    form.init();


Configuration
~~~~~~~~~~~~~

The Jinja macro supports parameters as follows (* indicates a required parameter)

+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    Parameter name    |                            Definition                                  |  Format              |                    Example                                         |
+======================+========================================================================+======================+====================================================================+
|    platform*         | Platform ID for the receiving device. Defaults to 'all'.               | String               | 'all', 'android', 'ios'                                            |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    product*          | Product ID for what should be downloaded. Defaults to 'firefox'.       | String               | 'firefox', 'focus', 'klar'                                         |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    message_set*      | ID for the email that should be received. Defaults to 'default'.       | String               | 'default', 'fx-mobile-download-desktop', 'download-firefox-rocket' |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    id*               | HTML form ID. Defaults to 'send-to-device'.                            | String               | 'send-to-device'                                                   |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    include_title     | Should the widget contain a title. Defaults to 'True'.                 | Boolean              | 'True', 'False'                                                    |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    title_text        | Provides a custom string for the form title, overriding the default.   | Localizable string   | _('Send Firefox Lite to your smartphone or tablet')                |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    input_label       | Provides a custom label for the input field, overriding the default.   | Localizable string   | _('Enter your email')                                              |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    legal_note_email  | Provides a custom legal note for email use.                            | Localizable String.  | _('The intended recipient of the email must have consented.')      |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    legal_note_sms    | Provides a custom legal note for SMS or email.                         | Localizable string   | _('SMS service available in select countries only.')               |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+
|    spinner_color     | Hex color for the form spinner. Defaults to '#000'.                    | String               | '#fff'                                                             |
+----------------------+------------------------------------------------------------------------+----------------------+--------------------------------------------------------------------+


Geolocation Callback
--------------------

You can piggy-back on the widget's geolocation call by providing a callback function to be executed when the lookup has completed::

  var form = new Mozilla.SendToDevice();
  form.geoCallback = function(countryCode) {
    console.log(countryCode);
  }
  form.init();

The callback function will be passed a single argument - the country code returned from the geolocation lookup.

If the geolocation lookup fails, the country code passed to the callback function will be an empty string.
