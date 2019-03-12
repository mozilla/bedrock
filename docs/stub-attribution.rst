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

For campaigns or experiments that originate on www.mozilla.org, Stub Attribution
requires some extra configuration. We want to avoid using first-party utm parameters
on mozilla.org pages, since those create new sessions in Google Analytics and can
confound data. To work around this, there is a custom stub attribution script that can
be used to pass custom data to the authentication service, avoiding the need for any
first-party utm parameters.

To use the custom attribution script, override the regular stub attribution block in
the page template where an experiment exists:

.. code-block:: html

    {% block stub_attribution %}
      <!--[if !lte IE 8]><!-->
      {{ js_bundle('stub-attribution-custom') }}
      {{ js_bundle('my-page-experiment-script') }}
      <!--<![endif]-->
    {% endblock %}

The `stub-attribution-custom` bundle contains the code that enables passing custom data
to the authentication service. You can then use that code in `my-page-experiment-script`,
or whatever you decide to call the experiment bundle:

.. code-block:: javascript

    var params = {
        utm_source: 'www.mozilla.org',
        utm_medium: 'download_button',
        utm_campaign: 'download_thanks_page',
        utm_content: 'download_thanks_install_experiment-v1'
    };

    // an optional callback for tracking when the experiment is seen in GA.
    function callback() {
        window.dataLayer.push({
            'data-ex-name': 'download_thanks_install_experiment',
            'data-ex-variant': 'v1'
        });
    }

    Mozilla.CustomStubAttribution.init(params, callback);

Authenticating custom data this way will override any existing stub attribution cookie
a visitor may have.

.. Note::

    There are some exceptions in the way that the custom attribution script behaves.
    Existing utm data will not be overwritten if there is already a `utm_content` parameter
    in the page URL. The custom attribution script will do nothing in this scenario. If
    any other utm parameters exist on the page URL, those will be passed through to the
    custom attribution script in favor of any custom values. This is to try and preserve
    as much existing information as possible, whilst still retaining the `utm_content`
    value that is essential to attributing an experiment.
