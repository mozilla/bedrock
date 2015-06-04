.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _testing:

==================
Functional testing
==================

Bedrock runs a suite of front-end functional tests using `CasperJS`_, which is powered by
a headless web browser called `PhantomJS`_.

Installation
------------

The specific version of CasperJS and PhantomJS needed to run the tests can be installed by running the
following command from the root directory of the project::

    npm install

.. Note::

    You may have already run ``npm install`` when initially setting up bedrock to run locally,
    in which case you can skip running this command again.

To confirm that you have PhantomJS installed correctly, you can run the following command::

    ./node_modules/.bin/phantomjs --version

This should output the following::

    1.9.8

To confirm that you have CasperJS installed and running together with the correct version
of PhantomJS, you can run the following command::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs

You should now see output similar to::

    CasperJS version 1.1.0-beta3 at /bedrock/node_modules/casperjs, using phantomjs version 1.9.8

Running tests
-------------

To run the functional tests against your local bedrock instance, type::

    npm test

This is a shortcut for the following command::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs test tests/functional --config=tests/config.json

This will run all test files found in the ``tests/functional`` directory and assumes you
have bedrock running at ``localhost`` on port ```8000``

To run a single test suite you can tell CasperJS to excecute a specific file e.g.::

    test tests/functional/home.js

You can also easily run the tests against any bedrock environment by specifying the domain.

For example, to run all functional tests against dev::

    test tests/functional --domain=https://www-dev.allizom.org

.. Note::

    Make sure to include the configuration file ``--config=tests/config.json`` when running tests.
    This is needed for PhantomJS to open certain URLs served over https.

Debugging
---------

You can enable logging on the command line by passing the following additional flags::

    --verbose --log-level=debug

.. _CasperJS: http://casperjs.org/
.. _PhantomJS: http://phantomjs.org/
.. _PhantomJS 1.9.8: https://bitbucket.org/ariya/phantomjs/downloads
