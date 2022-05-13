.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _pipeline:

===================================
Continuous Integration & Deployment
===================================

Bedrock runs a series of automated tests as part of continuous integration workflow and
`Deployment Pipeline`_. You can learn more about each of the individual test suites
by reading their respective pieces of documentation:

* Python unit tests (see :ref:`run-python-tests`).
* JavaScript unit tests (see :ref:`testing`).
* Redirect tests (see :ref:`testing-redirects`).
* Functional tests (see :ref:`testing`).

Tests in the lifecycle of a change
----------------------------------

Below is an overview of the tests during the lifecycle of a change to bedrock:

Local development
~~~~~~~~~~~~~~~~~

The change is developed locally, and page specific integration tests can be executed against a
locally running instance of the application. If testing changes to the website as a whole is
required, then pushing changes to the special ``run-integration-tests`` branch (see below) is
much faster than running the full test suite locally.

Pull request
~~~~~~~~~~~~

Once a pull request is submitted, `CircleCI`_ will run both the Python and JavaScript
unit tests, as well as the suite of redirect headless HTTP(s) response checks.

Push to main branch
~~~~~~~~~~~~~~~~~~~~~

Whenever a change is pushed to the main branch, a new image is built and deployed to the
dev environment, and the full suite of headless and UI tests are run. This is handled by the
pipeline, and is subject to change according to the settings in the `.gitlab-ci.yml file
in the www-config repository`_.

The tests for the dev environment are currently configured as follows:

- Chrome (latest) via local Selenium grid.
- Firefox (latest) via local Selenium grid.
- Internet Explorer 11 (smoke tests) via `Sauce Labs`_.
- Internet Explorer 9 (sanity tests) via `Sauce Labs`_.
- Headless tests.

If you view a job's `pipeline configuration`_, you will also notice there are manual tests
that can be run via SauceLabs for Firefox, Chrome, Edge, and Download tests. These tests
aren't run automatically and will not block a deployment, but they can be useful if you
want to run an extra set of checks should you see a test failure and want some verification.

Note that now we have Mozorg mode and Pocket mode, we actually stand up two dev, two stage
and two test deployments and we run the appropriate integration tests against each deployment:
most tests are written for Mozorg, but there are some for Pocket mode that also get run.

Push to stage branch
~~~~~~~~~~~~~~~~~~~~~

Whenever a change is pushed to the stage branch, a production docker image is built, published to
`Docker Hub`_, and deployed to a `public staging environment`_. Once the new image is deployed, the
full suite of UI tests is run against it again, but this time with the addition of the `headless
download tests`.

.. _tagged-commit:

Push to prod branch (tagged)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a tagged commit is pushed to the prod branch, a production docker image is built and published
to `Docker Hub`_ if needed (usually this will have already happened as a result of a push to the stage branch),
and deployed to each `production`_ deployment. After each deployment is complete, the full suite of UI tests is
run again (the same as for stage). As with untagged pushes, this is all handled by the pipeline, and is subject
to change according to the settings in the `.gitlab-ci.yml file in the www-config repository`_.

**Push to prod cheat sheet**

#. Check out the ``main`` branch
#. Make sure the ``main`` branch is up to date with ``mozilla/bedrock main``
#. Check that dev deployment is green:
    #. View `deployment pipeline`_ and look at ``main`` branch
#. Tag and push the deployment by running ``bin/tag-release.sh --push``

.. note::

    By default the ``tag-release.sh`` script will push to the ``origin`` git remote. If you'd
    like for it to push to a different remote name you can either pass in a ``-r`` or
    ``--remote`` argument, or set the ``MOZ_GIT_REMOTE`` environment variable. So the following
    are equivalent:

    .. code-block:: bash

        $ bin/tag-release.sh --push -r mozilla

    .. code-block:: bash

        $ MOZ_GIT_REMOTE=mozilla bin/tag-release.sh --push

    And if you'd like to just tag and not push the tag anywhere, you may omit the ``--push``
    parameter.


What Is Currently Deployed?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can look at the git log of the ``main`` branch to find the last commit with a date-tag on it (e.g. 2022-05-05):
this commit will be the last one that was deployed to production. You can also use the whatsdeployed.io service to get
a nice view of what is actually currently deployed to Dev, Stage, and Prod:

[![What's deployed on dev,stage,prod?](https://img.shields.io/badge/whatsdeployed-dev,stage,prod-green.svg)](https://whatsdeployed.io/s/RuO/mozilla/bedrock)


Instance Configuration & Switches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We have a `separate repo <https://github.com/mozmeao/www-config>`_ for configuring our primary instances (dev, stage, and prod).
The `docs for updating configurations <https://mozmeao.github.io/www-config/>`_ in that repo are on their own page,
but there is a way to tell what version of the configuration is in use on any particular instance of bedrock.
You can go to the ``/healthz-cron/`` URL on an instance (`see prod <https://www.mozilla.org/healthz-cron/>`_ for example) to see the current
commit of all of the external Git repos in use by the site and how long ago they were updated. The info on that page also includes the latest
version of the database in use, the git revision of the bedrock code, and how long ago the database was updated. If you recently made
a change to one of these repos and are curious if the changes have made it to production, this is the URL you should check.

Updating Selenium
~~~~~~~~~~~~~~~~~

There are several components for Selenium, which are independently versioned. The first is the Python client,
and this can be updated via the `test dependencies`_. The other components are the Selenium versions used in
both SauceLabs and the local Selenium grid. These versions are selected automatically based on the
required OS / Browser configuration, so they should not need to be updated or specified independently.

Adding test runs
~~~~~~~~~~~~~~~~

Test runs can be added by creating a new job in the `.gitlab-ci.yml file in the www-config repository`_
with the desired variables. For example, if you wanted to run the smoke tests in IE10, you could create the
following clauses:

.. code-block:: yaml

  .ie10:
    variables:
      BROWSER_NAME: internet explorer
      BROWSER_VERSION: "10.0"
      PLATFORM: Windows 8
      MARK_EXPRESSION: smoke

  test-ie10-saucelabs:
    extends:
      - .test
      - .ie10
      - .saucelabs

You can use `Sauce Labs platform configurator`_ to help with the parameter values.

Pushing to the integration tests branch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have commit rights to our Github repo (mozilla/bedrock) you can simply push
your branch to the branch named ``run-integration-tests``, and the app will be deployed
and the full suite of integration tests for that branch will be run. Please announce in
our Slack channel (#www on mozilla.slack.com) that you'll be doing this so
that we don't get conflicts. Also remember that you'll likely need to force push, as there
may be commits on that branch which aren't in yours – so, if you have the
``mozilla/bedrock`` remote set as ``mozilla``:

.. code-block:: bash

    $ git push -f mozilla your-local-branch-name-here:run-integration-tests


.. _Deployment Pipeline: https://gitlab.com/mozmeao/www-config/-/pipelines
.. _pipeline configuration: https://gitlab.com/mozmeao/www-config/-/pipelines/207024459
.. _CircleCI: https://circleci.com/
.. _Sauce Labs: https://saucelabs.com/
.. _.gitlab-ci.yml file in the www-config repository: https://github.com/mozmeao/www-config/tree/main/.gitlab-ci.yml
.. _test dependencies: https://github.com/mozilla/bedrock/blob/main/requirements/dev.txt
.. _Selenium Docker versions: https://hub.docker.com/r/selenium/hub/tags/
.. _Sauce Labs platform configurator: https://wiki.saucelabs.com/display/DOCS/Platform+Configurator/
.. _public staging environment: https://www.allizom.org
.. _Docker Hub: https://hub.docker.com/r/mozmeao/bedrock/tags
.. _production: https://www.mozilla.org
