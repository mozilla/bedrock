.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

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

The change is developed locally, and all integration tests can be executed against a
locally running instance of the application.

Pull request
~~~~~~~~~~~~

Once a pull request is submitted, `CircleCI`_ will run both the Python and  JavaScript
unit tests, as well as the suite of redirect headless HTTP(s) response checks.

Push to master branch
~~~~~~~~~~~~~~~~~~~~~

Whenever a change is pushed to the master branch, a new image is built and deployed to the
dev environment, and the full suite of headless and UI tests are then run against
Firefox on Windows 10 using `Sauce Labs`_. This is handled by the pipeline, and is subject
to change according to the settings in the `.gitlab-ci.yml file in the www-config repository`_.

Push to stage branch
~~~~~~~~~~~~~~~~~~~~~

Whenever a change is pushed to the stage branch, a production docker image is built, published to
`Docker Hub`_, and deployed to a `public staging environment`_. Once the new image is deployed, the
full suite of UI tests is run against it with Firefox, Chrome, and Internet Explorer on
Windows 10, and the sanity suite is run with IE9.

.. _tagged-commit:

Push to prod branch (tagged)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a tagged commit is pushed to the prod branch, a production docker image is built and published
to `Docker Hub`_ if needed (usually this will have already happened as a result of a push to the stage branch),
and deployed to each `production`_ deployment. After each deployment is complete, the full suite of UI tests is
run against Firefox, Chrome and Internet Explorer on Windows 10, and the sanity suite is run against IE9.
As with untagged pushes, this is all handled by the pipeline, and is subject
to change according to the settings in the `.gitlab-ci.yml file in the www-config repository`_.

**Push to prod cheat sheet**

#. Check out the ``master`` branch
#. Make sure the ``master`` branch is up to date with ``mozilla/bedrock master``
#. Check that dev deployment is green:
    #. View `deployment pipeline`_ and look at ``master`` branch
#. Tag and push the deployment by running ``bin/tag-release.sh --push``

.. note::

    By default the ``tag-release.sh`` script will push to the ``origin`` git remote. If you'd
    like for it to push to a different remote name you can either pass in a ``-r`` or
    ``--remote`` argument, or set the ``MOZ_GIT_REMOTE`` environment variable. So the following
    are equivalent::

        $ bin/tag-release.sh --push -r mozilla
        $ MOZ_GIT_REMOTE=mozilla bin/tag-release.sh --push

    And if you'd like to just tag and not push the tag anywhere, you may omit the ``--push``
    parameter.


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

There are two components for Selenium, which are independently versioned. The first is
the Python client, and this can be updated via the `test dependencies`_. The other
component is the server, which in the pipeline is either provided by a Docker container
or `Sauce Labs`_. The ``SELENIUM_VERSION`` environment variable controls both of these, and
they should ideally use the same version, however it’s possible that availability of
versions may differ. You can check the `Selenium Docker versions`_ available. If needed, the global
default can be set and then can be overridden in the individual job configuration.

Adding test runs
~~~~~~~~~~~~~~~~

Test runs can be added by creating a new job in the `.gitlab-ci.yml file in the www-config repository`_
with the desired variables. For example, if you wanted to run tests in Firefox on both Windows 10 and
OS X, against our dev environment, you could create the following clauses:

.. code-block:: yaml

  dev-test-firefox-osx:
    extends:
      - .dev
      - .test
    variables:
      BROWSER_NAME: firefox
      BROWSER_VERSION: latest
      PLATFORM: OS X 10.11

  dev-test-firefox-win10:
    extends:
      - .dev
      - .test
    variables:
      BROWSER_NAME: firefox
      BROWSER_VERSION: latest
      PLATFORM: Windows 10

You can use `Sauce Labs platform configurator`_ to help with the parameter values.

If you have commit rights to our Github repo (mozilla/bedrock) you can simply push
your branch to the branch named ``run-integration-tests``, and the ``bedrock-test.moz.works``
app will be deployed and the full suite of integration tests for that branch will be run.
Please announce in our Slack channel (#www on mozilla.slack.com) that you'll be doing this so
that we don't get conflicts.

.. _Deployment Pipeline: https://ci.vpn1.moz.works/blue/organizations/jenkins/bedrock_multibranch_pipeline/branches/
.. _CircleCI: https://circleci.com/
.. _Sauce Labs: https://saucelabs.com/
.. _Jenkinsfile: https://github.com/mozilla/bedrock/tree/master/Jenkinsfile
.. _branch-specific YAML files: https://github.com/mozilla/bedrock/tree/master/jenkins/branches/
.. _.gitlab-ci.yml file in the www-config repository: https://github.com/mozmeao/www-config/tree/master/.gitlab-ci.yml
.. _prod.yml file: https://github.com/mozilla/bedrock/tree/master/jenkins/branches/prod.yml
.. _bedrock_integration_tests_runner: https://ci.vpn1.moz.works/view/Bedrock/job/bedrock_integration_tests_runner/
.. _configured in Jenkins: https://ci.vpn1.moz.works/configure
.. _become unresponsive: https://issues.jenkins-ci.org/browse/JENKINS-28175
.. _test dependencies: https://github.com/mozilla/bedrock/blob/master/requirements/dev.txt
.. _Selenium Docker versions: https://hub.docker.com/r/selenium/hub/tags/
.. _Sauce Labs platform configurator: https://wiki.saucelabs.com/display/DOCS/Platform+Configurator/
.. _enhancement request: https://issues.jenkins-ci.org/browse/JENKINS-26210
.. _bug for the IRC plugin: https://issues.jenkins-ci.org/browse/JENKINS-28175
.. _public staging environment: https://www.allizom.org
.. _Docker Hub: https://hub.docker.com/r/mozmeao/bedrock/tags
.. _production: https://www.mozilla.org
