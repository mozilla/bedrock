.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

============================
Analytics
============================

Google Tag Manager (GTM)
------------------------

Bedrock uses Google Tag Manager (GTM) to manage and organize its Google Analytics solution.

GTM is a tag management system that allows for easy implementation of Google Analytics tags and other 3rd party marketing tags in a nice GUI experience. Tags can be added, updated, or removed directly from the GUI. GTM allows for a `one source of truth` approach to managing an analytics solution in that all analytics tracking can be inside GTM.

Bedrock's GTM solution is CSP compliant and does not allow for the injection of custom HTML or JavaScript but all tags use built in templates to minimize any chance of introducing a bug into Bedrock.

The GTM DataLayer
-----------------

How an application communicates with GTM is via the ``dataLayer`` object, which is a simple JavaScript array GTM instantiates on the page. Bedrock will send messages to the ``dataLayer`` object by means of pushing an object literal onto the ``dataLayer``. GTM creates an abstract data model from these pushed objects that consists of the most recent value for all keys that have been pushed to the ``dataLayer``.

The only reserved key in an object pushed to the ``dataLayer`` is ``event`` which will cause GTM to evaluate the firing conditions for all tag triggers.

DataLayer Push Example
----------------------

If we wanted to track clicks on a carousel and capture what the image was that was clicked, we might write a dataLayer push like this:

.. code-block:: javascript

    dataLayer.push({
        'event': 'carousel-click',
        'image': 'house'
    });

In the dataLayer push there is an event value to have GTM evaluate the firing conditions for tag triggers, making it possible to fire a tag off the dataLayer push. The event value is descriptive to the user action so it's clear to someone coming in later what the dataLayer push signifies. There is also an image property to capture the image that is clicked, in this example it's the house picture.

In GTM, a tag could be setup to fire when the event ``carousel-click`` is pushed to the dataLayer and could consume the image value to pass on what image was clicked.

The Core DataLayer Object
-------------------------

For the passing of contextual data on the user and page to GTM, we've created what we call the Core DataLayer Object. This object passes as soon as all required API calls for contextual data have completed. Unless there is a significant delay to when data will be available, please pass all contextual or meta data on the user or page here that you want to make available to GTM.

GTM Listeners & Data Attributes
-------------------------------

GTM also uses click and form submit listeners to gather context on what is happening on the page. Listeners push to the dataLayer data on the specific element that triggered the event, along with the element object itself.

Since GTM listeners pass the interacted element object to the dataLayer, the use of data attributes works very well when trying to identify key elements that you want to be tracked and for storing data on that element to be passed into Google Analytics. We use data attributes to track clicks on all downloads, buttons elements, and nav, footer, and CTA/button link elements.

.. Important::

    When adding any new elements to a Bedrock page, please follow the below guidelines to ensure accurate analytics tracking.

For all nav, footer, and CTA/button link elements, add these data attributes:

+--------------------------+--------------------------------+
|    Data Attribute        |        Expected Value          |
+==========================+================================+
|    data-link-type        | 'nav', 'footer', or 'button'   |
+--------------------------+--------------------------------+
|    data-link-name        | name or text of the link       |
+--------------------------+--------------------------------+

For all button elements, add this data attribute:

+--------------------------+--------------------------------+
|    Data Attribute        |        Expected Value          |
+==========================+================================+
|   data-button-name       | name or text of the link       |
+--------------------------+--------------------------------+

For all download buttons, add these data attributes:

+--------------------------+--------------------------------+
|    Data Attribute        |        Expected Value          |
+==========================+================================+
|    data-link-type        | 'Desktop', 'Android', or 'iOS' |
+--------------------------+--------------------------------+
|    data-download-os      | name or text of the link       |
+--------------------------+--------------------------------+
|   data-download-version  |'standard', 'developer', 'beta' |
+--------------------------+--------------------------------+

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
----------------------------------

``data-link-type="button"`` and ``data-link-name=""`` trigger a generic link
click with the following structure:

    | Event Category: {{page ID}} Interactions
    | Event Action: {{data-link-type}} click
    | Event Label: {{data-link-name}}

Any element that has a ``data-button-name=""`` triggers an event with this
structure:

    | Event Category: {{page ID}} Interactions
    | Event Action: button click
    | Event Label: {{data-button-name}}
