.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _banners:

=======
Banners
=======

Creating page banners
---------------------

Any page on bedrock can incorporate a top of page banner as a temporary feature.
An example of such a banner is the :abbr:`MOFO (Mozilla Foundation)` fundraising
form that gets shown on the home page several times a year.

Banners can be inserted into any page template by using the ``page_banner``
block. Banners can also be toggled on and off using a switch:

.. code-block:: jinja

    {% block page_banner %}
      {% if switch('fundraising-banner') %}
        {% include 'includes/banners/fundraiser.html' %}
      {% endif %}
    {% endblock %}

Banner templates should extend the *base banner template*, and content can
then be inserted using ``banner_title`` and  ``banner_content`` blocks:

.. code-block:: jinja

    {% extends 'includes/banners/base.html' %}

    {% block banner_title %}We all love the web. Join Mozilla in defending it.{% endblock %}

    {% block banner_content %}
        <!-- insert custom HTML here -->
    {% endblock %}

CSS styles for banners should be located in ``media/css/base/banners/``, and
should extend common base banner styles:

.. code-block:: css

    @import 'includes/base';

To initiate a banner on a page, include ``js/base/banners/mozilla-banner.js`` in
your page bundle and then initiate the banner using a unique ID. The ID will
be used as a cookie identifier should someone dismiss a banner and not wish to
see it again.

.. code-block:: javascript

    (function() {
        'use strict';

        function onLoad() {
            window.Mozilla.Banner.init('fundraising-banner');
        }

        window.Mozilla.run(onLoad);

    })();

By default, page banners will be rendered directly underneath the primary page navigation.
If you want to render a banner flush at the top of the page, you can pass a secondary
``renderAtTopOfPage`` parameter to the ``init()`` function with a boolean value:

.. code-block:: javascript

    (function() {
        'use strict';

        function onLoad() {
            window.Mozilla.Banner.init('fundraising-banner', true);
        }

        window.Mozilla.run(onLoad);

    })();

L10n for page banners
~~~~~~~~~~~~~~~~~~~~~

Because banners can technically be shown on any page, they need to be broadly
translated, or alternatively limited to the subset of locales that have
translations. Each banner should have its own ``.ftl`` associated
with it, and accessible to the template or view it gets used in.
