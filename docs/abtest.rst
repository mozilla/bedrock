.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _ab_testing:

===========
A/B Testing
===========

Traffic Cop experiments
-----------------------

More complex experiments, such as those that feature full page redesigns, or
multi-page user flows, should be implemented using `Traffic Cop
<https://github.com/mozmeao/trafficcop/>`_. Traffic Cop small javascript
library which will direct site traffic to different variants in a/b
experiments and make sure a visitor always sees the same variation.

It's possible to test more than 2 variants.

Traffic Cop sends users to experiments and then we use Google Analytics (GA) to
analyze which variation is more successful. (If the user has :abbr:`DNT (Do Not Track)`
enabled they do not participate in experiments.)

All a/b tests should have a `mana page <https://mana.mozilla.org/wiki/display/EN/Details+of+experiments+by+mozilla.org+team>`_
detailing the experiment and recording the results.

Coding the variants
~~~~~~~~~~~~~~~~~~~

Traffic cop supports two methods of a/b testing. Executing different on page
javascript or  redirecting to the same URL with a query string appended. We
mostly use the redirect method in bedrock. This makes testing easier.

Create a `variation view <http://bedrock.readthedocs.io/en/latest/coding.html#variation-views>`_
for the a/b test.

The view can handle the URL redirect in one of two ways:

#. the same page, with some different content based on the `variation` variable
#. a totally different page

Content variation
~~~~~~~~~~~~~~~~~

Useful for small focused tests.

This is explained on the `variation view <http://bedrock.readthedocs.io/en/latest/coding.html#variation-views>`_
page.

New page
~~~~~~~~

Useful for large page changes where content and assets are dramatically
different.

Create the variant page like you would a new page. Make sure it is ``noindex``
and does not have a ``canonical`` URL.

.. code-block:: jinja

    {% block canonical_urls %}<meta name="robots" content="noindex,follow">{% endblock %}


Configure as explained on the `variation view <http://bedrock.readthedocs.io/en/latest/coding.html#variation-views>`_
page.

Traffic Cop
~~~~~~~~~~~

Create a .js file where you initialize Traffic Cop and include that in the
experiments block in the template that will be doing the redirection. Wrap the
extra js include in a `switch <http://bedrock.readthedocs.io/en/latest/install.html#feature-flipping-aka-switches>`_.

.. code-block:: jinja

    {% block experiments %}
      {% if switch('experiment-berlin-video', ['de']) %}
        {{ js_bundle('firefox_new_berlin_experiment') }}
      {% endif %}
    {% endblock %}

Switches
~~~~~~~~

See the traffic cop section of the `switch docs <http://bedrock.readthedocs.io/en/latest/install.html#feature-flipping-aka-switches>`_ for instructions.

Recording the data
~~~~~~~~~~~~~~~~~~

.. Note::

    If you are measuring installs as part of your experiment be sure to configure `custom stub attribution <https://bedrock.readthedocs.io/en/latest/firefox-stub-attribution.html#measuring-campaigns-and-experiments>`_ as well.

Including the ``data-ex-variant`` and ``data-ex-name`` in the analytics
reporting will add the test to an auto generated report in :abbr:`GA (Google Analytics)`.
The variable values may be provided by the analytics team.

.. code-block:: javascript

    if (href.indexOf('v=a') !== -1) {
        // UA
        window.dataLayer.push({
            'data-ex-variant': 'de-page',
            'data-ex-name': 'Berlin-Campaign-Landing-Page'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'Berlin-Campaign-Landing-Page',
            variant: 'de-page',
        });
    } else if (href.indexOf('v=b') !== -1) {
        // UA
        window.dataLayer.push({
            'data-ex-variant': 'campaign-page',
            'data-ex-name': 'Berlin-Campaign-Landing-Page'
        });
        // GA4
        window.dataLayer.push({
            event: 'experiment_view',
            id: 'Berlin-Campaign-Landing-Page',
            variant: 'campaign-page',
        });
    }

Make sure any buttons and interaction which are being compared as part of the
test will report into :abbr:`GA (Google Analytics)`.

Viewing the data
~~~~~~~~~~~~~~~~~~

The ``data-ex-name`` and ``data-ex-variant`` are encoded in Google Analytics as custom dimensions 69 and 70.

Create a custom report.

Set the "Metrics Group" to include Sessions. Configure additional metrics depending on what the experiment was measuring (downloads, events, etc.)

Set the "Dimension Drilldowns to have cd69 in the top position and cd70 in the drilldown position.

View the custom report and drilldown into the experiment with the matching name.

Tests
~~~~~

Write some tests for your a/b test. This could be simple or complex depending
on the experiment.

Some things to consider checking:

- Requests for the default (non variant) page call the correct template.
- Requests for a variant page call the correct template.
- Locales excluded from the test call the correct (default) template.

A/B Test PRs that might have useful code to reuse
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- https://github.com/mozilla/bedrock/pull/5736/files
- https://github.com/mozilla/bedrock/pull/4645/files
- https://github.com/mozilla/bedrock/pull/5925/files
- https://github.com/mozilla/bedrock/pull/5443/files
- https://github.com/mozilla/bedrock/pull/5492/files
- https://github.com/mozilla/bedrock/pull/5499/files

Avoiding experiment collisions
------------------------------

To ensure that Traffic Cop doesn't overwrite data from any other externally
controlled experiments (for example Ad campaign tests, or in-product Firefox
experiments), you can use the experiment-utils helper to decide whether or
not Traffic Cop should initiate.

.. code-block:: javascript

    import TrafficCop = from '@mozmeao/trafficcop';
    import { isApprovedToRun } from '../../base/experiment-utils.es6';

    if (isApprovedToRun()) {
        const cop = new TrafficCop({
            id: 'experiment-name',
            variations: {
                'entrypoint_experiment=experiment-name&entrypoint_variation=a': 10,
                'entrypoint_experiment=experiment-name&entrypoint_variation=b': 10
            }
        });

        cop.init();
    }

The ``isApprovedToRun()`` function will check the page URL's query parameters
against a list of well-known experimental params, and return ``false`` if
any of those params are found. It will also check for some other cases where
we do not want to run experiments, such as if the page is being opened in
an automated testing environment.
