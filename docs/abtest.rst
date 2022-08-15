.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _ab_testing:

===========
A/B Testing
===========

Convert experiments
-------------------

Conversion rate optimization (CRO) experiments on bedrock are run on separate,
experimental versions of our main landing pages using a tool called
`Convert <https://convert.com>`_. Convert experiments are for relatively simple
multivariate experiments, such as testing changes to headlines, images, or
button copy.

Experimental versions of our main product pages can be found under the ``/exp/``
app within bedrock. We keep our main product pages separate from experiment
code for the following reasons:

- Performance (when an experiment is active, only those who qualify need download the Convert JS).
- Security (keeping the experimentation surface as small as required).

Creating experimental pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Templates within the ``/exp/`` app should have the following characteristics:

1. They should extend their respective jinja templates and live at a separate URL (e.g. /exp/firefox/new/ should extend /firefox/new/).

.. code-block:: jinja

    {% extends "firefox/new/desktop/download.html" %}

2. They should override the following blocks required to load Convert

.. code-block:: jinja

    {% block html_attrs %}{{ super() }} {% include 'exp/includes/id.html' %}{% endblock %}

    {% block experiments %}
        {% include 'exp/includes/convert.html' %}
    {% endblock %}

    {% block stub_attribution %}
        {% include 'exp/includes/stub.html' %}
    {% endblock %}

3. If a page is indexed by search engines, then the experimental equivalent should have a canonical URL that points back to the original page. If the page is considered to be an in-product page, then the experimental page should retain the same noindex meta tag.

.. code-block:: jinja

    {% block canonical_urls %}
        <link rel="canonical" href="{{ settings.CANONICAL_URL }}/{{ LANG }}/firefox/new/">
    {% endblock %}

4. Experimental pages should also contain an Open Graph sharing URL that points back to the original page.

.. code-block:: jinja

    {% block page_og_url %}{{ settings.CANONICAL_URL }}/{{ LANG }}/firefox/new/{% endblock %}

Once an experimental page exists, A/B tests can then be implemented using
the `Convert dashboard <https://convert.com>`_ and editor. Convert
experiments should be coded and tested against staging, before being
reviewed and scheduled to run in production.

QA for Convert experiments
~~~~~~~~~~~~~~~~~~~~~~~~~~

The process for QA'ing Convert experiments is as follows:

#. Experiments are completely built and configured to run on ``https://www.allizom.org/*``
#. In the Github issue for an experiment, someone will request review by an engineer.

An engineer reviewing the experiment will:

#. Verify that the experiment is not configured to run on https://www.mozilla.org/ (production) yet.
#. Activate the experiment to run on stage.

During review, the engineer will compare the following to the experiment plan:

#. The experiment’s logic.
#. Any JS included (in Convert editor’s JS field).
#. Any CSS included (in Convert editor’s CSS field).
#. The target audience is configured.
#. The goals are configured.
#. The distribution percentages are configured.
#. The target URLs are configured.

Once the engineer is satisfied, the engineer (or someone else with write privileges) will:

#. Add ``https://www.mozilla.org/*`` to the list of URLs the experiment can run on.
#. Reset the experiment (eliminating any data gathered during QA).
#. Activate (or schedule) the experiment.

.. Note::

    ``*`` should be replaced by the exact URL pathname for the experiment page.

Routing traffic to experimental pages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once an experimental page has been created, a predefined percentage of traffic
can then be redirected from the main product page, to the experimental page
using a `Cloudflare Worker <https://workers.cloudflare.com/>`_ script. We do
this using a worker because it has significant performance improvements over
doing redirection on the client or the server, and can also be done
independently of a bedrock deployment.

The code for redirecting to experimental pages lives in the
`www-workers <https://github.com/mozmeao/www-workers>`_ repository.

Adding a new redirect requires making a pull request to add a new object to
the ``experimentalPages`` array in the ``workers/redirector.js`` file. An
existing configuration to route 6% of traffic from ``/firefox/new/`` to
``/exp/firefox/new/`` can be seen below:

.. code-block:: javascript

    const experimentPages = [
        {
            'targetPath': `/en-US/firefox/new/`,
            'sandboxPath': `/en-US/exp/firefox/new/`,
            'sampleRate': 0.06
        }
    ];

.. Important::

    When implementing new changes to the redirector, make sure to test and
    verify that things are working as expected on dev and stage before
    pushing to production. See the documentation in the
    `www-workers <https://github.com/mozmeao/www-workers>`_ repository for
    more information.

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

    If you are measuring installs as part of your experiment be sure to configure `custom stub attribution <https://bedrock.readthedocs.io/en/latest/stub-attribution.html#measuring-campaigns-and-experiments>`_ as well.

Including the ``data-ex-variant`` and ``data-ex-name`` in the analytics
reporting will add the test to an auto generated report in :abbr:`GA (Google Analytics)`.
The variable values may be provided by the analytics team.

.. code-block:: javascript

    if (href.indexOf('v=a') !== -1) {
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

Make sure any buttons and interaction which are being compared as part of the
test and will report into :abbr:`GA (Google Analytics)`.

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
