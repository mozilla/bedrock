.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _firefox-accounts:

============================
Firefox Accounts Signup Form
============================

Introduction
------------

Certain bedrock pages such as ``/firefox/accounts`` and ``/firefox/firstrun`` feature a
Firefox Accounts signup form using an embedded ``iframe``. To test the signup flow on
a non-production environment requires some additional Firefox profile configuration.

Local Development
-----------------

#. Set ``FXA_IFRAME_SRC`` in your ``.env`` file to point to the FXA development server:

    ``FXA_IFRAME_SRC=https://stomlinson.dev.lcip.org/``

#. Set your local development server to run on ``127.0.0.1:8111``.
#. Quit Firefox.
#. Create a new profile for testing called ``FxA Test Local`` by following the
   `instructions here`_.
#. In the new profile folder, create a file called ``user.js`` and paste in the
   following content:

    .. code-block:: javascript

        user_pref("services.sync.log.appender.file.logOnSuccess", true);
        user_pref("identity.fxaccounts.auth.uri", "https://stomlinson.dev.lcip.org/auth/v1");
        user_pref("identity.fxaccounts.remote.force_auth.uri", "https://stomlinson.dev.lcip.org/force_auth?service=sync&context=fx_desktop_v1");
        user_pref("identity.fxaccounts.remote.signin.uri", "https://stomlinson.dev.lcip.org/signin?service=sync&context=fx_desktop_v1");
        user_pref("identity.fxaccounts.remote.signup.uri", "https://stomlinson.dev.lcip.org/signup?service=sync&context=fx_desktop_v1");
        user_pref("identity.fxaccounts.settings.uri", "https://stomlinson.dev.lcip.org/settings");
        user_pref("identity.fxaccounts.remote.webchannel.uri", "https://stomlinson.dev.lcip.org/");
        user_pref("services.sync.tokenServerURI", "https://stomlinson.dev.lcip.org/syncserver/token/1.0/sync/1.5");

        user_pref("general.warnOnAboutConfig", false);
        user_pref("devtools.chrome.enabled", true);
        user_pref("devtools.debugger.remote-enabled", true);

#. Start Firefox using the new profile created in step 3.
#. Verify the FxA settings look correct by opening ``about:config`` and searching for
   ``identity.fxaccounts``.
#. Navigate to the web page containing the form and test signing up.

Demo Server Testing
-------------------

#. Quit Firefox.
#. Create a new profile for testing called ``FxA Test Demo`` by following the
   `instructions here`_.
#. In the new profile folder, create a file called ``user.js`` and paste in the
   following content:

    .. code-block:: javascript

        user_pref("services.sync.log.appender.file.logOnSuccess", true);
        user_pref("identity.fxaccounts.auth.uri", "https://api-accounts.stage.mozaws.net/v1");
        user_pref("identity.fxaccounts.remote.force_auth.uri", "https://accounts.stage.mozaws.net/force_auth?service=sync&context=fx_desktop_v1");
        user_pref("identity.fxaccounts.remote.signin.uri", "https://accounts.stage.mozaws.net/signin?service=sync&context=fx_desktop_v1");
        user_pref("identity.fxaccounts.remote.signup.uri", "https://accounts.stage.mozaws.net/signup?service=sync&context=fx_desktop_v1");
        user_pref("identity.fxaccounts.settings.uri", "https://accounts.stage.mozaws.net/settings");
        user_pref("identity.fxaccounts.remote.webchannel.uri", "https://accounts.stage.mozaws.net/");
        user_pref("services.sync.tokenServerURI", "https://token.stage.mozaws.net/1.0/sync/1.5");

        user_pref("general.warnOnAboutConfig", false);
        user_pref("devtools.chrome.enabled", true);
        user_pref("devtools.debugger.remote-enabled", true);

#. Start Firefox using the new profile you created in step 2.
#. Verify the FxA settings look correct by opening ``about:config`` and searching for
   ``identity.fxaccounts``.
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
