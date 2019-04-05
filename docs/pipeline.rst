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
unit tests, as well as the smoke suite of redirect headless HTTP(s) response checks.

Push to master branch
~~~~~~~~~~~~~~~~~~~~~

Whenever a change is pushed to the master branch, a new image is built and deployed to the
dev environment, and the full suite of headless and UI tests are then run against
Firefox on Windows 10 using `Sauce Labs`_. This is handled by the pipeline, and is subject
to change according to the settings in the `master.yml file`_ in the repository.

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
to change according to the settings in the `prod.yml file`_ in the repository.

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

Pipeline integration
--------------------

Our `Jenkinsfile`_ will run the integration tests based on information in our `branch-specific YAML files`_.
These files specify various test names per branch that will cause it to use different
parameters, allowing it to be called in many different ways to cover the testing
needs. The job executes `this script <https://github.com/mozilla/bedrock/blob/master/docker/bin/run_integration_tests.sh>`_,
which then runs `this Docker image <https://github.com/mozilla/bedrock/blob/master/docker/dockerfiles/bedrock_test>`_,
and ultimately runs `another script <https://github.com/mozilla/bedrock/blob/master/bin/run-integration-tests.sh>`_.
The two scripts can also be executed locally to replicate the way Jenkins operates.

During the **Test Images** stage, the Test Runner job is called without a ``BASE_URL``. This means
that a local instance of the application will be started, and the URL of this instance
will be used for testing. The ``DRIVER`` parameter is set to ``Remote``, which causes a
local instance of Selenium Grid to be started in Docker and used for the browser-based
functional UI tests.

The test scripts above will be run once for each properties name specified in the `branch-specific YAML files`_
for the branch being built and tested. Pushes to `master` will run different tests than pushes to `prod`
for example.

Configuration
~~~~~~~~~~~~~

Many of the options are configured via environment variables passed from the initial
script to the Docker image and onto the final script. Many of these options can be
set in the `branch-specific YAML files`_ in the repository. In the `branch-specific YAML files`_
folder you can copy any file there to match the name of your branch and modify it
to set how it should be built by jenkins. Take the following example:

.. code-block:: yaml

    # jenkins/branches/change-all-the-things.yml
    smoke_tests: true
    apps:
      - bedrock-probably-broken

This configuration would cause commits pushed to a branch named ``change-all-the-things`` to have docker
images built for them, have the smoke and unit tests run, and deploy to a deis app named ``bedrock-probably-broken``
in our us-west deis cluster. If you'd like it to create the deis app and pre-fill a local database for your app,
you can set ``demo: true`` in the file. Note that if the app already exists it must have the ``jenkins`` user added via the
``deis perms:create jenkins -a <your app name>`` command.

The available branch configuration options are as follows:

* ``smoke_tests``: boolean. Set to ``true`` to cause the unit and smoke test suites run against the docker images.
* ``push_public_registry``: boolean. Set to ``true`` to cause the built images to be pushed to the public docker hub.
* ``require_tag``: boolean. Set to ``true`` to require that the commit being built have a git tag in the format YYYY-MM-DD.X.
* ``regions``: list. A list of strings indicating the deployment regions for the set of apps. The valid values are in the ``regions`` area of
  the ``jenkins/global.yml`` file. If omitted a deployment to only ``oregon-b`` is assumed.
* ``apps``: list. A list of strings indicating the deis app name(s) to which to deploy. If omitted no deployments will occur.
* ``demo``: boolean. Set to ``true`` to have the deployed app in demo mode, which means it will have a pre-filled local
  database and the deis app will be created and configured for you if it doesn't already exist.
* ``integration_tests``: list. A list of strings indicating the types of integration tests to run. If omitted no tests will run.

.. _configure-demo-servers:

Configure Demo Servers
~~~~~~~~~~~~~~~~~~~~~~

You can also set app configuration environment variables via deployment as well for demos. The default environment variables
are set in `jenkins/branches/demo/default.env`. To modify your app's settings you can create an env file named after your branch
(e.g `jenkins/branches/demo/pmac-l10n.env` for the branch `demo/pmac-l10n.env`). The combination
of values from `demo/default.env`, your branch specific env file, and a region specific env file (e.g. `jenkins/regions/virginia.env`)
will be used to configure the app. So you only need to add the variables that differ from the default files to your file,
and you can override any values from the default files as well.

Instance Configuration & Switches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Beyond setting environment variables in demo instances as described above, we have a `separate repo <https://github.com/mozmeao/www-config>`_
for configuring our primary instances (dev, stage, and prod). The `docs for updating configurations <https://mozmeao.github.io/www-config/>`_
in that repo are on their own page, but there is a way to tell what version of the configuration is in use on any particular instance of bedrock.
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

Test runs can be added by creating a new properties section in the
`integration tests script <https://github.com/mozilla/bedrock/blob/master/docker/bin/run_integration_tests.sh>`_
with the parameters of the new test run. This is simply a bash script and you can duplicate a clause of the case staement.
For example, if you wanted to run tests in Firefox on both Windows 10 and
OS X, you could create the following clauses:

.. code-block:: bash

    case $1 in
      osx-firefox)
        BROWSER_NAME=firefox
        PLATFORM="OS X 10.11"
        ;;
      win10-firefox)
        BROWSER_NAME=firefox
        PLATFORM="Windows 10"
        ;;

You can use `Sauce Labs platform configurator`_ to help with the parameter values.

If you have commit rights to our Github repo (mozilla/bedrock) you can simply push
your branch to the branch named ``run-integration-tests``, and the ``bedrock-integration-tests``
app will be deployed and all of the integration tests defined in the ``jenkins.yml``
file for that branch will be run. Please announce in our IRC channel (#www on irc.mozilla.org)
that you'll be doing this so that we don't get conflicts.

Known issues in Jenkins
-----------------------

Jenkins stalls after global configuration changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using the IRC plugin for notifications, global configuration changes can cause
Jenkins to become unresponsive. To make such changes it can be necessary to first
restart Jenkins, as this issue only appears some time after Jenkins has been started.
A `bug for the IRC plugin`_ has been raised.

.. _Deployment Pipeline: https://ci.vpn1.moz.works/blue/organizations/jenkins/bedrock_multibranch_pipeline/branches/
.. _CircleCI: https://circleci.com/
.. _Sauce Labs: https://saucelabs.com/
.. _Jenkinsfile: https://github.com/mozilla/bedrock/tree/master/Jenkinsfile
.. _branch-specific YAML files: https://github.com/mozilla/bedrock/tree/master/jenkins/branches/
.. _master.yml file: https://github.com/mozilla/bedrock/tree/master/jenkins/branches/master.yml
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
.. _Docker Hub: https://hub.docker.com/r/mozorg/bedrock/tags
.. _production: https://www.mozilla.org
