.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillanotificationbanner:

===========================
Mozilla Notification Banner
===========================

``mozilla-notification-banner.js`` is a JavaScript library for displaying custom in-page notifications at the top of bedrock web pages. It can be used globally across the site for display over multiple pages, or on a page-by-page basis. It is also capable of displying multiple variations of a notification for A/B testing purposes.

Dependencies
------------

The notification library requires some additional CSS & JS dependencies:

    - ``css/base/notification-banner.less``
    - ``css/pebbles/components/_notification-banner.scss``
    - ``js/base/mozilla-cookie-helper.js``

.. note::

    All of the above dependencies are currently bundled in all of bedrock's common CSS & JS bundles by default, so they should not need including on a page-by-page basis.

Usage
-----

To configure a notification, it must be passed one or more ``config`` objects. Each ``config`` is an object literal that relates to a specific message that may be shown to a visitor::

    var config = {
        'id': 'fx-out-of-date-banner',
        'name': 'fx-out-of-date',
        'heading': 'Your Firefox is out-of-date.',
        'message': 'Get the most recent version to keep browsing securely.',
        'confirm': 'Update Firefox',
        'confirmClick': _clickCallback,
        'url': '/firefox/download/thanks/',
        'close': closeText,
        'gaConfirmAction': 'Update Firefox',
        'gaConfirmLabel': 'Firefox for Desktop',
        'gaCloseLabel': 'Close'
    };

This object must then be passed to initialize the notification for display::

    Mozilla.NotificationBanner.init(config);

As long as all the requirements of the config are satisfied, this should be all that's needed in order for the notification to appear. If any of the requirements are not satisifed, the notification will not display. A full list of available options are provided below.

Options
~~~~~~~

- ``id`` (required) - Unique identifier used to track variations a visitor has seen e.g. ``fx-out-of-date-banner-copy1-direct-1``.
- ``name`` (required) - Generic name for the notification type e.g. ``fx-out-of-date``.
- ``experimentName`` (optional) - Generic name for tracking a specific experiment in GA e.g. ``fx-out-of-date-banner-copy1``.
- ``experimentVariant`` (optional) - Identifier for experiment variation in GA e.g. ``direct-1``.
- ``heading`` (required) - Copy string for notification heading.
- ``message`` (required) - Copy string for notification message / subheading.
- ``confirm`` (required) - Copy string for main CTA button.
- ``url`` (required) - URL for main CTA link.
- ``close`` (required) - Copy string for close button.
- ``gaConfirmAction`` (required) - String for action of CTA button in GA (this should always be English).
- ``gaConfirmLabel`` (required) - String for labeling CTA button in GA (this should always be English).
- ``gaCloseLabel`` (required) - String for labeling close button in GA (this should always be English).
- ``confirmClick`` (optional) - Callback to be executed on confirm CTA click.

Persistent notifications
~~~~~~~~~~~~~~~~~~~~~~~~

A notification will be displayed on every visit to a web page where it is instantiated, until a visitor interacts with it either by clicking the main call-to-action button, or closing the notifiction via the close button. Once a visitor interacts with a notification, it will not be displayed again for a **default 21 day** time period (set via a cookie).

This default expriy date can be changed manually if required::

    Mozilla.NotificationBanner.COOKIE_EXPIRATION_DAYS = 28;

Testing multiple variations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To test multiple variations of messaging in a notification, you can also pass an array of ``options`` objects to ``getOptions``::

    var options = [
        {
            'id': 'fx-out-of-date-banner-copy1-direct-1',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'direct-1',
            'heading': 'Your browser security is at risk.',
            'message': 'Update Firefox now to protect yourself from the latest malware.',
            'confirm': 'Update now',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'confirmClick': _clickCallback,
            'url': '/firefox/download/thanks/',
            'close': 'Close',
            'closeLabel': 'Close'
        },
        {
            'id': 'fx-out-of-date-banner-copy1-direct-2',
            'name': 'fx-out-of-date',
            'experimentName': 'fx-out-of-date-banner-copy1',
            'experimentVariant': 'direct-2',
            'heading': 'Your Firefox is out-of-date.',
            'message': 'Get the most recent version to keep browsing securely.',
            'confirm': 'Update Firefox',
            'confirmAction': 'Update Firefox',
            'confirmLabel': 'Firefox for Desktop',
            'confirmClick': _clickCallback,
            'url': '/firefox/download/thanks/',
            'close': 'Close',
            'closeLabel': 'Close'
        },
    ];

    var choice = Mozilla.NotificationBanner.getOptions(options);

    if (choice) {
        Mozilla.NotificationBanner.init(choice);
    }

Calling ``Mozilla.NotificationBanner.getOptions(options)`` will pick a variation at random to display if no variation has already been seen. When a visitor sees a random variation, a cookie will be stored with a reference to it's ``id``. This ``id`` is used on repeat visits to ensure that the same variation gets shown again, should the visitor not interact with the notification.

Setting a sample rate
~~~~~~~~~~~~~~~~~~~~~

You can also set a sample rate limit, if you wish for only a finite percentage of visitors to see a notification::

    Mozilla.NotificationBanner.setSampleRate(0.05); // 5% sample rate

.. note::

    By default there is no sample rate set, so a notification will display 100% of the time.
