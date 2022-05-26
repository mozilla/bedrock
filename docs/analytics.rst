.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _analytics:

============================
Analytics
============================

Google Tag Manager (GTM)
------------------------

Bedrock uses Google Tag Manager (GTM) to manage and organize its Google Analytics solution.

:abbr:`GTM (Google Tag Manager)` is a tag management system that allows for easy implementation of Google Analytics tags and other 3rd party marketing tags in a nice :abbr:`GUI (Graphical User Interface)` experience. Tags can be added, updated, or removed directly from the GUI. GTM allows for a "one source of truth" approach to managing an analytics solution in that all analytics tracking can be inside GTM.

Bedrock's :abbr:`GTM (Google Tag Manager)` solution is :abbr:`CSP (Content Security Policy)` compliant and does not allow for the injection of custom HTML or JavaScript but all tags use built in templates to minimize any chance of introducing a bug into Bedrock.

The :abbr:`GTM (Google Tag Manager)` DataLayer
----------------------------------------------

How an application communicates with :abbr:`GTM (Google Tag Manager)` is via the ``dataLayer`` object, which is a simple JavaScript array GTM instantiates on the page. Bedrock will send messages to the ``dataLayer`` object by means of pushing an object literal onto the ``dataLayer``. GTM creates an abstract data model from these pushed objects that consists of the most recent value for all keys that have been pushed to the ``dataLayer``.

The only reserved key in an object pushed to the ``dataLayer`` is ``event`` which will cause :abbr:`GTM (Google Tag Manager)` to evaluate the firing conditions for all tag triggers.

DataLayer Push Example
----------------------

If we wanted to track clicks on a carousel and capture what the image was that was clicked, we might write a dataLayer push like this:

.. code-block:: javascript

    dataLayer.push({
        'event': 'carousel-click',
        'image': 'house'
    });

In the dataLayer push there is an event value to have :abbr:`GTM (Google Tag Manager)` evaluate the firing conditions for tag triggers, making it possible to fire a tag off the dataLayer push. The event value is descriptive to the user action so it's clear to someone coming in later what the dataLayer push signifies. There is also an image property to capture the image that is clicked, in this example it's the house picture.

In :abbr:`GTM (Google Tag Manager)`, a tag could be setup to fire when the event ``carousel-click`` is pushed to the dataLayer and could consume the image value to pass on what image was clicked.

The Core DataLayer Object
-------------------------

For the passing of contextual data on the user and page to :abbr:`GTM (Google Tag Manager)`, we've created what we call the Core DataLayer Object. This object passes as soon as all required API calls for contextual data have completed. Unless there is a significant delay to when data will be available, please pass all contextual or meta data on the user or page here that you want to make available to GTM.

:abbr:`GTM (Google Tag Manager)` Listeners & Data Attributes
------------------------------------------------------------

:abbr:`GTM (Google Tag Manager)` also uses click and form submit listeners to gather context on what is happening on the page. Listeners push to the dataLayer data on the specific element that triggered the event, along with the element object itself.

Since :abbr:`GTM (Google Tag Manager)` listeners pass the interacted element object to the dataLayer, the use of data attributes works very well when trying to identify key elements that you want to be tracked and for storing data on that element to be passed into Google Analytics. We use data attributes to track clicks on all downloads, buttons elements, and nav, footer, and :abbr:`CTA (Call To Action)`/button link elements.

.. Important::

    When adding any new elements to a Bedrock page, please follow the below guidelines to ensure accurate analytics tracking.

For all generic :abbr:`CTA (Call To Action)` links and <button> elements, add these data attributes (* indicates a required attribute):

+--------------------------+---------------------------------------------------------------------+
|    Data Attribute        |        Expected Value (lowercase)                                   |
+==========================+=====================================================================+
|    data-cta-type *       | Link type (e.g. 'navigation', 'footer', or 'button')                |
+--------------------------+---------------------------------------------------------------------+
|    data-cta-text         | name or text of the link                                            |
+--------------------------+---------------------------------------------------------------------+
|    data-cta-position     | Location of CTA on the page (e.g. 'primary', 'secondary', 'header') |
+--------------------------+---------------------------------------------------------------------+

For Firefox download buttons, add these data attributes (* indicates a required attribute). Note that ``data-download-name`` and ``data-download-version`` should be included for download buttons that serve multiple platforms. For mobile specific store badges, they are not strictly required.

+---------------------------+-----------------------------------------------------------------------------------------------+
|    Data Attribute         |        Expected Value                                                                         |
+===========================+===============================================================================================+
|    data-link-type *       | 'download'                                                                                    |
+---------------------------+-----------------------------------------------------------------------------------------------+
|    data-download-os *     | 'Desktop', 'Android', 'iOS'                                                                   |
+---------------------------+-----------------------------------------------------------------------------------------------+
|    data-download-name     | 'Windows 32-bit', 'Windows 64-bit', 'macOS', 'Linux 32-bit', 'Linux 64-bit', 'iOS', 'Android' |
+---------------------------+-----------------------------------------------------------------------------------------------+
|    data-download-version  | 'win', 'win64', 'osx', 'linux', 'linux64', 'ios', 'android'                                   |
+---------------------------+-----------------------------------------------------------------------------------------------+
|    data-download-location | 'primary', 'secondary', 'nav', 'other'                                                        |
+---------------------------+-----------------------------------------------------------------------------------------------+

For all links to accounts.firefox.com use these data attributes (* indicates a required attribute):

+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|    Data Attribute        |        Expected Value                                                                                                                                                                                              |
+==========================+====================================================================================================================================================================================================================+
|    data-cta-type *       | fxa-servicename (e.g. 'fxa-sync', 'fxa-monitor', 'fxa-lockwise')                                                                                                                                                   |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|    data-cta-text         | Name or text of the link (e.g. 'Sign Up', 'Join Now', 'Start Here'). We use this when the link text is not useful, as is the case with many FxA forms that say, 'Continue'. We replace 'Continue' with 'Register'. |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
|    data-cta-position     | Location of CTA on the page (e.g. 'primary', 'secondary', 'header')                                                                                                                                                |
+--------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

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


Some notes on how this looks in :abbr:`GA (Google Analytics)`
-------------------------------------------------------------

``data-cta-type=""`` and ``data-cta-name=""`` trigger a generic link / buton
click with the following structure:

    | Event Category: {{page ID}} Interactions
    | Event Action: {{data-cta-type}} click
    | Event Label: {{data-cta-name}}

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

Debugging Pings
~~~~~~~~~~~~~~~

For all non-production environments, bedrock will automatically set a debug
view tag for all pings. This means that when running on localhost, on a demo,
or on a staging environment, ping data will not be sent to the production data
pipeline. Instead, it will be sent to the `Glean debug dashboard`_ which can
be used to test that pings are working correctly. All bedrock debug pings will
register in the debug dashboard with the tag name ``moz-bedrock``.

Logging Pings in the Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running bedrock locally, you can also set the following environment variable
in your ``.env``` file to automatically log pings in the browser's web console.
This can be especially useful when making updates to analytics code.

.. code-block::

    GLEAN_LOG_PINGS=True

Defining Metrics and Pings
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

.. _Glean: https://docs.telemetry.mozilla.org/concepts/glean/glean.html
.. _Glean Book: https://mozilla.github.io/glean/book/index.html
.. _Glean debug dashboard: https://debug-ping-preview.firebaseapp.com/
.. _data review: https://wiki.mozilla.org/Data_Collection
