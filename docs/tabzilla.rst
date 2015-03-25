.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _tabzilla:
.. highlight:: c

========
Tabzilla
========

*Tabzilla* is the universal tab displayed on Mozilla websites.

Adding the universal tab to a site requires:

1. Add the static tab link (example below) to the top of your template::

    <a href="https://www.mozilla.org/" id="tabzilla">mozilla</a>

2. Include the tabzilla CSS by adding the following tag inside the ``<head>`` of your template::

    <link href="https://mozorg.cdn.mozilla.net/media/css/tabzilla-min.css" rel="stylesheet" />

3. Include the tabzilla.js file in your template (preferably just before the ``</body>``)::

    <script src="https://mozorg.cdn.mozilla.net/tabzilla/tabzilla.js"></script>

   This will choose the best locale for your visitor. If you prefer to force the locale, you can use::

    <script src="https://mozorg.cdn.mozilla.net/{locale}/tabzilla/tabzilla.js"></script>

   Where ``{locale}`` is the language in which you'd like Tabzilla to be loaded (e.g. fr or de).
   If Tabzilla is not yet translated into said locale the user will get the en-US version.

.. note:: Tabzilla uses jQuery. If your site already includes jQuery be sure to
          place the Tabzilla script tag **after** the one for jQuery. Tabzilla will
          use the existing jQuery if available and a supported version, otherwise
          it will load its own version of jQuery.

That the source file URLs begin with ``//`` is not a typo. This is a
protocol-relative URL which allows the resource to be loaded via
whichever protocol (http or https) the page itself is loaded. This
removes the need to add any logic to support loading Tabzilla over
both secure and insecure connections, thereby avoiding mixed-content
warnings from the browser.


Requirements
------------

As the universal tab does inject HTML/CSS into the DOM, some there are some requirements that you must meet.

- Background images must not be attached to the ``<body>`` element.
- Absolutely positioned elements must not be positioned relative to the ``<body>`` element.
- An element other than the ``<body>`` should add a 2 pixel white border to the top of the page (``border-top: 2px solid #fff;``)

Any background image or absolutely positioned element attached to the ``body`` element would not move with the rest of the contents when the tab slides open. Instead, any such background or element should be attached to anoter HTML element in the page (a wrapper div, for example). Note that this issue does not apply to solid background colors, or backgrounds that do not vary vertically (solid vertical stripes, for example).

If jQuery is already included on the page, it will be used by Tabzilla. If jQuery is not already on the page, it will automatically be included after the page has loaded.


Translation Bar
---------------

Tabzilla has an opt-in extension called *Translation Bar* that automatically offers a link to a localized page, if available, based on the user's locale. It is intended to improve international user experience. 

Adding the Translation Bar extension to Tabzilla requires:

1. Include `alternate URLs <https://support.google.com/webmasters/answer/189077>`_ in the ``<head>`` element. For example::

    <link rel="alternate" hreflang="en-US" href="http://www.mozilla.org/en-US/firefox/new/" title="English (US)">
    <link rel="alternate" hreflang="fr" href="http://www.mozilla.org/fr/firefox/new/" title="Français">

   The Translation Bar alternatively detects available translations by looking for a language switcher like below, but implementation of alternate URLs is recommended also from the SEO perspective::

    <select id="language"><option value="en-US">English (US)</option></select>

2. Add the ``data-infobar`` attribute to the tab link, with the ``translation`` option::

    <a href="https://www.mozilla.org/" id="tabzilla" data-infobar="translation">mozilla</a>

.. note:: Though the Translation Bar is currently implemented as an extension of Tabzilla, it might be moved to a standalone language utility in the future.


Update Bar
---------------

This is another information bar intended to improve user security. It checks if the user is using the latest Firefox version, and if not, prompts the user to update the browser.

Adding the Update Bar extension to Tabzilla requires:

1. Add the ``data-infobar`` attribute to the tab link, with the ``update`` option::

    <a href="https://www.mozilla.org/" id="tabzilla" data-infobar="update translation">mozilla</a>

The value of the ``data-infobar`` attribute is the order of priority. You can enable both the Update Bar and Translation Bar as the example above, but one information bar will be shown at a time.
