.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _tabzilla:
.. highlight:: c

========
Tabzilla
========

*tabzilla* is the universal tab displayed on Mozilla websites.

Adding the universal tab to a site requires:

1. Add the static tab link (example below) to the top of your template::

    <a href="http://www.mozilla.org/" id="tabzilla">mozilla</a>

2. Include the tabzilla.css CSS file either as a CSS include or built in to your minified styles::
    
    <link href="//www.mozilla.org/media/css/tabzilla-min.css" rel="stylesheet" />

3. Include the tabzilla.js file in your template (preferably in the footer)::

    <script src="//www.mozilla.org/tabzilla/tabzilla.js"></script>

   This will choose the best locale for your visitor. If you prefer to force the locale, you can use::

    <script src="//www.mozilla.org/{locale}/tabzilla/tabzilla.js"></script>


Requirements
------------

As the universal tab does inject HTML/CSS into the DOM, some there are some requirements that you must meet.

- Background images must not be attached to the ``<body>`` element.
- Absolutely positioned elements must not be positioned relative to the ``<body>`` element.
- An element other than the ``<body>`` should add a 2 pixel white border to the top of the page (``border-top: 2px solid #fff;``)

Any background image or absolutely positioned element attached to the ``body`` element would not move with the rest of the contents when the tab slides open. Instead, any such background or element should be attached to anoter HTML element in the page (a wrapper div, for example). Note that this issue does not apply to solid background colors, or backgrounds that do not vary vertically (solid vertical stripes, for example).

If jQuery is already included on the page, it will be used by Tabzilla. If jQuery is not already on the page, it will automatically be included after the page has loaded.
