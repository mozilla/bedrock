.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _analytics:

=================
Website analytics
=================

***********
Mozorg Mode
***********

Google Tag Manager (GTM)
------------------------

In mozorg mode, bedrock uses `Google Tag Manager (GTM)`_ to manage and organize
its `Google Analytics`_ solution.

:abbr:`GTM (Google Tag Manager)` is a tag management system that allows for
easy implementation of Google Analytics (GA) tags and other 3rd party marketing
tags in a nice :abbr:`GUI (Graphical User Interface)` experience. Tags can be
added, updated, or removed directly from the GUI. GTM allows for a "one
source of truth" approach to managing an analytics solution in that all
analytics tracking can be inside GTM.

Bedrock's GTM solution is :abbr:`CSP (Content Security Policy)` compliant and
does not allow for the injection of custom HTML or JavaScript but all tags use
built in templates to minimize any chance of introducing a bug into Bedrock.

The GTM DataLayer
~~~~~~~~~~~~~~~~~

How an application communicates with GTM is via the ``dataLayer`` object, which
is  a simple JavaScript array GTM instantiates on the page. Bedrock will send
messages to the ``dataLayer`` object by means of pushing an object literal onto
the ``dataLayer``. GTM creates an abstract data model from these pushed objects
that consists of the most recent value for all keys that have been pushed to
the ``dataLayer``.

The only reserved key in an object pushed to the ``dataLayer`` is ``event`` which
will cause GTM to evaluate the firing conditions for all tag triggers.

DataLayer push example
~~~~~~~~~~~~~~~~~~~~~~

If we wanted to track clicks on a carousel and capture what the image was that
was clicked, we might write a dataLayer push like this:

.. code-block:: javascript

    dataLayer.push({
        'event': 'carousel-click',
        'image': 'house'
    });

In the dataLayer push there is an event value to have GTM evaluate the firing
conditions for tag triggers, making it possible to fire a tag off the dataLayer
push. The event value is descriptive to the user action so it's clear to someone
coming in later what the dataLayer push signifies. There is also an image property
to capture the image that is clicked, in this example it's the house picture.

In GTM, a tag could be setup to fire when the event ``carousel-click`` is pushed
to the dataLayer and could consume the image value to pass on what image was clicked.

The Core DataLayer object
~~~~~~~~~~~~~~~~~~~~~~~~~

For the passing of contextual data on the user and page to GTM, we've created what we
call the Core DataLayer Object. This object passes as soon as all required API calls
for contextual data have completed. Unless there is a significant delay to when data
will be available, please pass all contextual or meta data on the user or page here
that you want to make available to GTM.

GTM listeners & data attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GTM also uses click and form submit listeners to gather context on what is happening
on the page. Listeners push to the dataLayer data on the specific element that
triggered the event, along with the element object itself.

Since GTM listeners pass the interacted element object to the dataLayer, the use of
data attributes works very well when trying to identify key elements that you want to
be tracked and for storing data on that element to be passed into Google Analytics. We
use data attributes to track clicks on all downloads, buttons elements, and nav, footer,
and :abbr:`CTA (Call To Action)`/button link elements.

.. Important::

    When adding any new elements to a Bedrock page, please follow the below guidelines
    to ensure accurate analytics tracking.

For all generic CTA links and ``<button>`` elements, add these data attributes
(* indicates a required attribute):

+-----------------------+---------------------------------------------------------------------------+
| Data Attribute        | Expected Value (lowercase)                                                |
+=======================+===========================================================================+
| ``data-cta-type`` *   | Link type (e.g. ``navigation``, ``footer``, or ``button``)                |
+-----------------------+---------------------------------------------------------------------------+
| ``data-cta-text``     | name or text of the link                                                  |
+-----------------------+---------------------------------------------------------------------------+
| ``data-cta-position`` | Location of CTA on the page (e.g. ``primary``, ``secondary``, ``header``) |
+-----------------------+---------------------------------------------------------------------------+

For Firefox download buttons, add these data attributes (* indicates a required attribute).
Note that ``data-download-name`` and ``data-download-version`` should be included for download
buttons that serve multiple platforms. For mobile specific store badges, they are not strictly
required.

+----------------------------+-------------------------------------------------------------------------------------------------------------+
| Data Attribute             | Expected Value                                                                                              |
+============================+=============================================================================================================+
| ``data-link-type`` *       | ``download``                                                                                                |
+----------------------------+-------------------------------------------------------------------------------------------------------------+
| ``data-download-os`` *     | ``Desktop``, ``Android``, ``iOS``                                                                           |
+----------------------------+-------------------------------------------------------------------------------------------------------------+
| ``data-download-name``     | ``Windows 32-bit``, ``Windows 64-bit``, ``macOS``, ``Linux 32-bit``, ``Linux 64-bit``, ``iOS``, ``Android`` |
+----------------------------+-------------------------------------------------------------------------------------------------------------+
| ``data-download-version``  | ``win``, ``win64``, ``osx``, ``linux``, ``linux64``, ``ios``, ``android``                                   |
+----------------------------+-------------------------------------------------------------------------------------------------------------+
| ``data-download-location`` | ``primary``, ``secondary``, ``nav``, ``other``                                                              |
+----------------------------+-------------------------------------------------------------------------------------------------------------+

For all links to accounts.firefox.com use these data attributes (* indicates a required attribute):

+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Data Attribute        | Expected Value                                                                                                                                                                                                                 |
+=======================+================================================================================================================================================================================================================================+
| ``data-cta-type`` *   | fxa-servicename (e.g. ``fxa-sync``, ``fxa-monitor``)                                                                                                                                                                           |
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``data-cta-text``     | Name or text of the link (e.g. ``Sign Up``, ``Join Now``, ``Start Here``). We use this when the link text is not useful, as is the case with many FxA forms that say, ``Continue``. We replace ``Continue`` with ``Register``. |
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``data-cta-position`` | Location of CTA on the page (e.g. ``primary``, ``secondary``, ``header``)                                                                                                                                                      |
+-----------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

For all conditional banners, add the following calls.

When a banner is shown:

.. code-block:: javascript

    dataLayer.push({
        'eLabel': 'Banner Impression',
        'data-banner-name': '<banner name>', //ex. Fb-Video-Compat
        'data-banner-impression': '1',
        'event': 'non-interaction'
    });

When an element in the banner is clicked:

.. code-block:: javascript

    dataLayer.push({
        'eLabel': 'Banner Clickthrough',
        'data-banner-name': '<banner name>', //ex. Fb-Video-Compat
        'data-banner-click': '1',
        'event': 'in-page-interaction'
    });

When a banner is dismissed:

.. code-block:: javascript

    dataLayer.push({
        'eLabel': 'Banner Dismissal',
        'data-banner-name': '<banner name>', //ex. Fb-Video-Compat
        'data-banner-dismissal': '1',
        'event': 'in-page-interaction'
    });


When doing a/b tests configure something like the following.

.. code-block:: javascript

    if(href.indexOf('v=a') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'de-page',
            'data-ex-name': 'Berlin-Campaign-Landing-Page'
        });
    } else if (href.indexOf('v=b') !== -1) {
        window.dataLayer.push({
            'data-ex-variant': 'campaign-page',
            'data-ex-name': 'Berlin-Campaign-Landing-Page'
        });
    }


Some notes on how this looks in GA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``data-cta-type=""`` and ``data-cta-name=""`` trigger a generic link / buton
click with the following structure:

- Event Category: ``{{page ID}} Interactions``
- Event Action: ``{{data-cta-type}} click``
- Event Label: ``{{data-cta-name}}``

How can visitors opt out of GA?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Visitors to the website can opt-out of loading Google Analytics on our
website by enabling `Do Not Track (DNT)`_ in their web browser. We
facilitate this by using a `DNT helper`_ that our team maintains.

Glean
-----

Currently in an evaluation phase, bedrock is now capable of running a parallel
first-party analytics implementation alongside :abbr:`GTM (Google Tag Manager)`,
using Mozilla's own `Glean`_ telemetry :abbr:`SDK (Software Development Kit)`.
See the `Glean Book`_ for more developer reference documentation.

Glean is currently behind a feature switch called ``SWITCH_GLEAN_ANALYTICS``.
When the switch is enabled pages will load the Glean JavaScript bundle,
which will do things like register page views and capture link clicks. Our
implementation leverages the same HTML data attributes that we use for
:abbr:`GTM (Google Tag Manager)` when tracking link clicks, so any attributes
you add for :abbr:`GTM (Google Tag Manager)` should also be captured by Glean
automatically.

Debugging pings
~~~~~~~~~~~~~~~

For all non-production environments, bedrock will automatically set a debug
view tag for all pings. This means that when running on localhost, on a demo,
or on a staging environment, ping data will not be sent to the production data
pipeline. Instead, it will be sent to the `Glean debug dashboard`_ which can
be used to test that pings are working correctly. All bedrock debug pings will
register in the debug dashboard with the tag name ``bedrock``.

Logging pings in the console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running bedrock locally, you can also set the following environment variable
in your ``.env``` file to automatically log pings in the browser's web console.
This can be especially useful when making updates to analytics code.

.. code-block::

    GLEAN_LOG_PINGS=True

Defining metrics and pings
~~~~~~~~~~~~~~~~~~~~~~~~~~

All of the data we send to the Glean pipeline is defined in
:abbr:`YAML (Yet Another Markup Language)` schema files in the ``./glean/``
project root directory. The ``metrics.yaml`` file defines all the different
metrics types we record, and the ``pings.yaml`` file defines the name of each
ping event we use to send collections of individual metrics. These are all
automatically documented in ``./glean/docs/``.

.. Note::

   Before running any Glean commands locally, always make sure you have first
   activated your virtual environment by running ``pyenv activate bedrock``.

When bedrock starts, we automatically run ``npm run glean`` which parses these
schema files and then generates some JavaScript library code in
``./media/js/libs/glean/``. This library code is not committed to the repository
on purpose, in order to avoid people altering it and becoming out of sync with
the schema. This library code is then imported into our Glean analytics code in
``./media/js/glean/``, which is where we initiate page views and capture click
events.

Running ``npm run glean`` can also be performed independently of starting bedrock.
It will also first lint the schema files.

.. Important::

    All metrics and pings we record using Glean must first undergo a `data review`_
    before being made active in production. Therefore anytime we make new additions
    to these files, those changes should also undergo review.

Using Glean pings in individual page bundles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All of our analytics code for Glean lives in a single bundle in the base template,
which is intended to be shared across all web pages. There may be times where we
want to send a ping from some JavaScript that exists only in a certain page
specific bundle however. For instances like this, there is a global ``pageEventPing``
helper available, which you can call from inside any custom event handler you write.

For user initiated events, such as clicks:

.. code-block:: javascript

    if (typeof window.Mozilla.Glean !== 'undefined') {
        window.Mozilla.Glean.pageEventPing({
            label: 'Newsletters: mozilla-and-you',
            type: 'Newsletter Signup Success'
        });
    }

For non-interaction events that are not user initiated:

.. code-block:: javascript

    if (typeof window.Mozilla.Glean !== 'undefined') {
        window.Mozilla.Glean.pageEventPing({
            label: 'Auto Play',
            type: 'Video'
            nonInteraction: true
        });
    }

How can visitors opt out of Glean?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Website visitors can opt out of Glean by visiting the first party `data preferences page`_,
which is linked to in the `websites privacy notice`_. Clicking opt-out will set a
cookie which Glean checks for before initializing on page load. In production, the
cookie that is set applies for all ``.mozilla.org`` domains, so other sites such as
``developer.mozilla.org`` can also make use of the opt-out mechanism.

***********
Pocket mode
***********

Google Tag Manager (GTM)
------------------------

In pocket mode, bedrock also uses Google Tag Manager (GTM) to manage and organize
its Google Analytics (GA4) solution. This is mostly for marketing's own use, and
is not used by the Pocket organization.

In contrast to mozorg mode, GA in Pocket is mostly used for measuring a few key
events, such as sign ups and logged-in / logged-out page views. Most of this event
and triggering logic exists entirely inside GTM, as opposed to in bedrock code.

Snowplow
--------

`Snowplow`_ is the analytics tool used by the Pocket organization, which is something
marketing has limited access to. Snowplow is mostly used for tracking events in the
Pocket web application, although we do also load it on the logged-out marketing
pages that are hosted by bedrock.

How can visitors opt out of Pocket analytics?
---------------------------------------------

Pocket website visitors can opt-out of both GA and Snowplow by changing their
preferences in the `One Trust Cookie Banner`_ we display on page load. If someone
opts-out of analytics cookies, we do not load GA, however we do still load Snowplow
in a more privacy reserved mode.

Snowplow configuration with cookie consent (default):

.. code-block:: javascript

    {
        appId: SNOWPLOW_APP_ID,
        platform: 'web',
        eventMethod: 'beacon',
        respectDoNotTrack: false,
        stateStorageStrategy: 'cookieAndLocalStorage',
        contexts: {
            webPage: true,
            performanceTiming: true
        },
        anonymousTracking: false
    }

Snowplow configuration without cookie consent:

.. code-block:: javascript

    {
        appId: SNOWPLOW_APP_ID,
        platform: 'web',
        eventMethod: 'post',
        respectDoNotTrack: false,
        stateStorageStrategy: 'none',
        contexts: {
            webPage: true,
            performanceTiming: true
        },
        anonymousTracking: {
            withServerAnonymisation: true
        }
    }

See our `Pocket analytics code`_ for more details.

.. _Google Tag Manager (GTM): https://tagmanager.google.com/
.. _Google Analytics: https://analytics.google.com/
.. _Do Not Track (DNT): https://support.mozilla.org/en-US/kb/how-do-i-turn-do-not-track-feature
.. _DNT helper: https://github.com/mozmeao/dnt-helper
.. _Glean: https://docs.telemetry.mozilla.org/concepts/glean/glean.html
.. _Glean Book: https://mozilla.github.io/glean/book/index.html
.. _Glean debug dashboard: https://debug-ping-preview.firebaseapp.com/
.. _data review: https://wiki.mozilla.org/Data_Collection
.. _data preferences page: https://www.mozilla.org/privacy/websites/data-preferences/
.. _websites privacy notice: https://www.mozilla.org/privacy/websites/
.. _Snowplow: https://snowplow.io/
.. _One Trust Cookie Banner: https://www.onetrust.com/
.. _Pocket analytics code: https://github.com/mozilla/bedrock/blob/main/media/js/pocket/analytics.es6.js



