.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _testing:

==================
Functional testing
==================

Bedrock runs a suite of front-end functional tests using `CasperJS`_, which is powered by
a headless web browser called `PhantomJS`_. These tests live in the ``tests`` directory.

The ``tests`` directory comprises of:

* ``/functional`` contains individual CasperJS test suites.
* ``/lib`` contains various ``config`` and ``helpers`` functions used to run the tests.
* ``config.json`` a configuration file used by PhantomJS when running tests.

Installation
------------

The specific version of CasperJS and PhantomJS needed to run the tests can be installed
by running the following command from the root directory of the project::

    npm install

.. Note::

    You may have already done ``npm install`` when initially setting up bedrock to run
    locally, in which case you can likely skip running this command again.

To confirm that you have PhantomJS installed correctly, you can run::

    ./node_modules/.bin/phantomjs --version

This should output the following::

    1.9.8

To confirm that you have CasperJS installed and running together with the correct version
of PhantomJS, you can run::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs

You should see output that starts with something similar to::

    CasperJS version 1.1.0-beta3 at /bedrock/node_modules/casperjs, using phantomjs version 1.9.8

Running tests
-------------

.. Note::

  Before running the tests, please make sure to follow the bedrock :ref:`installation
  docs<install>`, including the database sync that is needed to pull in external data such
  as event/blog feeds etc. These are required for some of the tests to pass.

To run the full functional test suite against your local bedrock instance, type::

    npm test

This is just a simple shortcut for the following command::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs test tests/functional --config=tests/config.json

This will run all test suites found in the ``tests/functional`` directory and assumes you
have bedrock running at ``localhost`` on port ``8000``.

To run a single test suite you must tell CasperJS to execute a specific file
e.g. ``tests/functional/home.js``::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs test tests/functional/home.js --config=tests/config.json

You can also easily run the tests against any bedrock environment by specifying the
``--domain`` variable. For example, to run all functional tests against dev::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs test tests/functional --domain=https://www-dev.allizom.org --config=tests/config.json

.. Note::

    ``npm test`` is just a simple shortcut and not something you can pass options to. If
    you want to specify a particular file to run or a different domain, you must use the
    full command like in the examples above. Also, make sure to include the configuration
    file ``--config=tests/config.json`` when running tests, as this is sometimes needed
    for PhantomJS to open certain URLs served over https.

Writing tests
-------------

Tests usually consist of telling CasperJS to open a web page, then verifying things you
expect to exist, and clicking does what you expect. An example test is as follows:

.. code-block:: javascript

    casper.test.begin('test example: ' + url, 2, function suite(test) {

        casper.start(url, function() {
            test.assertNotVisible('#some-element', 'Element is not visible initially');
            this.click('#some-button');
        });

        casper.waitUntilVisible('#some-element', function() {
            test.assert(true, 'Element is visible after button was clicked');
        });

        casper.run(function() {
            test.done();
            helpers.done();
        });
    });

.. note::

    It is important to call ``helpers.done();`` at the end of each test. This makes sure
    things such as viewport size and user agent are reset after each test completes.

Please take some time to read over the `CasperJS documentation`_ for details on the testing API.

Debugging
---------

You can enable logging on the command line by passing the following additional flags::

    --verbose --log-level=debug

Guidelines for writing tests
----------------------------

* Try and keep tests organized and cleanly separated. Each page should have its own test file, and each test should be responsible for a specific purpose, or component of a page.
* Avoid using generic timeouts. Always use CasperJS methods such as ``waitUntilVisible``, ``waitForSelector``, ``waitForUrl`` etc.
* Don't nest callbacks. Try and keep a flat hierarchy for async functions to avoid tests exiting early.
* Don't make tests overly specific. If a test keeps failing because of generic changes to a page such as an image filename or ``href`` being updated, then the test is probably too specific.
* Avoid string checking as tests may break if strings are updated, or could change depending on the page locale.
* If you write something reusable, consider adding it to ``helpers.js`` or ``config.js``.
* When writing tests, try and run them against a staging or demo environment in addition to local testing.

.. _CasperJS: http://casperjs.org/
.. _CasperJS documentation: http://casperjs.readthedocs.org/en/latest/
.. _PhantomJS: http://phantomjs.org/
.. _PhantomJS 1.9.8: https://bitbucket.org/ariya/phantomjs/downloads
