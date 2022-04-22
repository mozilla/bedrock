.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _browser_support:

===============
Browser Support
===============

We seek to provide usable experiences of our most important web content to all user agents.
But newer browsers are far more capable than older browsers, and the capabilities they
provide are valuable to developers and site visitors. We **will** take advantage of modern
browser capabilities. Older browsers **will** have a different experience of the website than
newer browsers. We will strike this balance by generally adhering to the core principles of
`Progressive Enhancement <https://en.wikipedia.org/wiki/Progressive_enhancement>`_:

    * Basic content should be accessible to all web browsers
    * Basic functionality should be accessible to all web browsers
    * Sparse, semantic markup contains all content
    * Enhanced layout is provided by externally linked CSS
    * Enhanced behavior is provided by unobtrusive, externally linked JavaScript
    * End-user web browser preferences are respected

Some website experiences may require us to deviate from these principles -- imagine *a
marketing campaign page built under timeline pressure to deliver novel functionality to a
particular locale for a short while* -- but those will be exceptions and rare.

Browser Support Matrix (Updated 2021-12-07)
-------------------------------------------

We deliver enhanced CSS & JS to browsers in our browser support matrix (below).
We deliver degraded support to all other user agents, except legacy IE browsers,
which get basic support.

**The following browsers have enhanced support:**

  * All evergreen browsers (Firefox, Chrome, Safari, Edge, Opera, etc.)
  * IE11 and above.

**The following browsers have degraded support:**

  * Outdated evergreen browser versions.
  * IE10.

**The following browsers have basic support:**

  * IE9 and below.

Delivering basic support
------------------------

On IE browsers that support `conditional comments`_ (IE9 and below), basic support
consists of no page-specific CSS or JS. Instead, we deliver well formed semantic HTML,
and a universal CSS stylesheet that gets applied to all pages. We do not serve these
older browsers any JS, with the exception of the following scripts:

  * Google Analytics / :abbr:`GTM (Google Tag Manager)` snippet.
  * HTML5shiv for parsing modern HTML semantic elements.
  * Stub Attribution script (IE8 / IE9).

Conditional comments should instead be used to handle content specific to IE. To hide
non-relevant content from IE users who see the universal stylesheet, a ``hide-from-legacy-ie``
class name can also be applied directly to HTML:

.. code-block:: html

    <p class="hide-from-legacy-ie">See what Firefox has blocked for you</p>

.. _conditional comments: https://wikipedia.org/wiki/Conditional_comment

Delivering degraded support
---------------------------

On other legacy browsers where conditional comments are not supported, developers should
instead rely on `feature detection`_ to deliver a degraded experience where appropriate.

.. _feature detection: https://developer.mozilla.org/docs/Learn/Tools_and_testing/Cross_browser_testing/Feature_detection

Feature detection using CSS
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For CSS, enhanced experiences can be delivered using `feature queries`_, whilst allowing
older browsers to degrade gracefully using simpler layouts when needed.

Additionally, there is also a universal CSS class hook available that gets delivered via
a site-wide JS feature detection snippet:

.. code-block:: css

    .is-modern-browser {
        /* Styles will only be applied to browsers that get enhanced support. */
    }

.. _feature queries: https://developer.mozilla.org/docs/Web/CSS/@supports

Feature detection using JavaScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For JS, enhanced support can be delivered using a helper that leverages the same
feature detection snippet:

.. code-block:: javascript

    (function() {
        'use strict';

        function onLoad() {
            // Code that will only be run on browsers that get enhanced support.
        }

        window.Mozilla.run(onLoad);
    })();

The ``site.isModernBrowser`` global property can also be used within conditionals like so:

.. code-block:: javascript

    if (window.site.isModernBrowser) {
        // Code that will only be run on browsers that get enhanced support.
    }

Exceptions (Updated 2019-06-11)
-------------------------------

Some pages of the website provide critical functionality to older browsers. In particular,
the Firefox desktop download funnel enables users on older browsers to get a modern browser.
To the extent possible, we try to deliver enhanced experiences to all user agents on these
pages.

**The following pages get enhanced experiences for a longer list of user agents:**

  * /firefox/
  * /firefox/new/
  * /firefox/download/thanks/

.. Note::

    An enhanced experience can be defined as a step above basic support. This can be achieved
    by delivering extra page-specific CSS to legacy browsers, or allowing them to degrade
    gracefully. It does not mean everything needs to `look the same in every browser`_.

.. _look the same in every browser: http://dowebsitesneedtolookexactlythesameineverybrowser.com/
