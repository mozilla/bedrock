.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _mozillatrafficcop:

===================
Mozilla Traffic Cop
===================

``mozilla-traffic-cop.js`` handles redirecting users to different A/B/x
variations through a query parameter.

.. note::

    ``mozilla-traffic-cop.js`` requires ``mozilla-cookie-helper.js``, which is
    included by default in the ``site.js`` bundle for most pages.

How It Works
------------

.. Important::

    The Traffic Cop will not initialize for users with DNT enabled.

After verifying the configuration, the Traffic Cop first makes sure the user is
not currently viewing a variation (to avoid a redirect loop). It then chooses a
random percentage (1-100).

If the percentage falls within the total percentage targeted by the config, it
will choose the appropriate variation and redirect the user.

If the percentage exceeds that of the config, no redirect will occur. (This
could be considered the "control".)

If a variation is chosen, a cookie is set that will send the user back to the
same variation if/when the page is again visited. (See below for setting cookie
duration.)

Any query string parameters present when a user initially lands on a page will be
propagated to the variation redirect.

Configuration
-------------

Each instance of the Traffic Cop requires two pieces of configuration:

- A string ID that is unique to other currently running tests (to avoid confusion when reading cookies)
- A variations object that lists all variations by query string along with the associated visitor percentage

An implementation might look like:

.. code-block:: javascript

    var eddie = new Mozilla.TrafficCop({
        id: 'exp_firefox_new_headline',
        variations: {
            'v=1': 25,
            'v=2': 25,
            'v=3': 25
        }
    });

    eddie.init();

In the above example, the string "exp_firefox_new_headline" will be used as the
cookie name should a variation be chosen.

The test will have 3 variations, each targeting 25% of users.

There is also an optional configuration value to specify how long the cookie
associated with a visitor for an individual experiment will last:
``cookieExpires``. This value must be a ``Number`` and represents the number of
hours the cookie will last. If omitted, the cookie will last for 24 hours. A
value of 0 will result in a session-length cookie.

An implementation with ``cookieExpires`` set might look like:

.. code-block:: javascript

    var lou = new Mozilla.TrafficCop({
        id: 'exp_mozorg_homepage_spring_2017',
        cookieExpires: 48, // 2 days
        variations: {
            'v=1': 25,
            'v=2': 25,
            'v=3': 25
        }
    });

    lou.init();

How a Variation is Chosen
-------------------------

Variations are sorted in the order provided, and percentages are tallied to
create tiers. Take the following config:

.. code-block:: javascript

    var rex = new Mozilla.TrafficCop({
        id: 'exp_firefox_new_headline',
        variations: {
            'v=c': 25,
            'v=a': 25,
            'v=f': 25
        }
    });

The implied tiers would be:

- ``v=c``: 1-25
- ``v=a``: 26-50
- ``v=f``: 51-75
- (no redirect): 76-100

So, if the random percentage chosen was 44, the user would be redirected to
``{current url}?v=a``.

Implementation
--------------

To add a Traffic Cop to a page, create a new JS bundle for the experiment that
includes:

- ``mozilla-traffic-cop.js``
- A new JS file that configures and initializes the experiment

.. Important::

    Place this new bundle in the ``experiments`` block of the page, wrapped in a
    ``switch`` for easy enabling and disabling:

    .. code-block:: jinja

        {% block experiments %}
          {% if switch('experiment-firefox-new') %}
             {% javascript 'experiment-firefox-new' %}
          {% endif %}
        {% endblock %}

What It Doesn't Do
------------------

No further user segmentation is handled by the Traffic Cop. This means that any
locale, OS, browser, or other restrictions must be handled elsewhere - i.e. in
the configuration JS file. Commonly requested features will likely be added to
the library as usage dictates.
