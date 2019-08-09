.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _browser_support:

=================
Browser Support
=================

We seek to provide usable experiences of our most important web content to all user agents. But newer browsers are far more capable than older browsers, and the capabilities they provide are valuable to developers and site visitors. We **will** take advantage of modern browser capabilities. Older browsers **will** have a different experience of the website than newer browsers. We will strike this balance by generally adhering to the core principles of `Progressive Enhancement <https://en.wikipedia.org/wiki/Progressive_enhancement>`_::

    * Basic content should be accessible to all web browsers
    * Basic functionality should be accessible to all web browsers
    * Sparse, semantic markup contains all content
    * Enhanced layout is provided by externally linked CSS
    * Enhanced behavior is provided by unobtrusive, externally linked JavaScript
    * End-user web browser preferences are respected

Some website experiences may require us to deviate from these principles -- imagine *a marketing campaign page built under timeline pressure to deliver novel functionality to a particular locale for a short while* -- but those will be exceptions and rare.

Technical details
-------------------

We deliver enhanced CSS & JS to browsers in our browser support matrix (below). We deliver basic support to all other user agents.

Basic support consists of no page-specific CSS or JS. Instead, we deliver basic semantic HTML, a universal CSS stylesheet that gets applied to all pages, and a universal JS bundle that only handles downloading Firefox (click a button, get a file), and Google Analytics.

Browser Support Matrix (Updated 20190809)
-------------------

**The following browsers have enhanced support:**

  * All evergreen browsers (Firefox, Chrome, Safari, Edge, Opera, etc.)
  * IE9 and above.

**The following browsers have basic support:**

  * All other IE browsers.

Exceptions (Updated 20190809)
-------------------
Some pages of the website provide critical functionality to older browsers. In particular, the Firefox desktop download funnel enables users on older browsers to get a modern browser. To the extent possible, we try to deliver enhanced experiences to all user agents on these pages.

**The following pages get enhanced support for a longer list of user agents:**

  * www.mozilla.org/firefox/new/
  * www.mozilla.org/firefox/download/thanks/

Future Support (Updated 20190809)
-------------------
The audience visiting in IE9 and IE10 is small and growing smaller. In late 2019 these browsers will be moved to the basic support list.
