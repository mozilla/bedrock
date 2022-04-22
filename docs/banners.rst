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

To initiate a banner on a page, include ``media/js/base/mozilla-banner.js`` in
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

Becuase banners can technically be shown on any page, they need to be broadly
translated, or alternatively limited to the subset of locales that have
translations. Each banner should have its own ``.lang`` or ``.ftl`` associated
with it, and accessible to the template or view it gets used in.

Fundraising banner
------------------

The fundraising banner typically gets shown on the home page, but
technically can be shown on any page in bedrock. The donation
parameters that get passed to the form require some extra context
data that needs to get passed to the template via the view in order
to work. For example:

.. code-block:: python

    def home_view(request):
        locale = l10n_utils.get_locale(request)
        donate_params = settings.DONATE_PARAMS.get(
            locale, settings.DONATE_PARAMS['en-US'])

        # presets are stored as a string but, for the home banner
        # we need it as a list.
        donate_params['preset_list'] = donate_params['presets'].split(',')

        ctx = {
            'donate_params': donate_params
        }

        return l10n_utils.render(request, 'mozorg/home/home.html', ctx)

The HTML and CSS assets for the fundraising banner are located in:

- ``bedrock/base/templates/includes/banners/fundraiser.html``
- ``media/css/base/banners/fundraiser.scss``

.. note::

    Strings for the fundraising banner are currently in a bit of a mess.
    Some are in ``main.lang``, whilst others are in the homepage ``.lang``
    file. This means it can't be shown outside of the home page currently,
    unless in English only. This needs fixing when we migrate over to Fluent.
