.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _testing:

=================
Front-end testing
=================

Bedrock runs a suite of front-end functional tests using `CasperJS`_, which is powered by
a headless web browser called `PhantomJS`_. We also have an additional suite of `Jasmine`_
behavioral/unit tests, which use `Karma`_ as a test runner. All these test suites live in
the ``tests`` directory.

The ``tests`` directory comprises of:

* ``/functional`` contains individual CasperJS test suites.
* ``/unit`` contains the Jasmine tests and Karma config file.
* ``/lib`` contains various ``config`` and ``helpers`` functions used to run the functional tests.
* ``config.json`` a configuration file used by PhantomJS when running tests.

Installation
------------

The specific versions of CasperJS, PhantomJS and Jasmine/Karma which are needed to run the
tests, can be installed by running the following command from the root directory of the project::

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

Running CasperJS tests
----------------------

.. Note::

  Before running the CasperJS tests, please make sure to follow the bedrock :ref:`installation
  docs<install>`, including the database sync that is needed to pull in external data such
  as event/blog feeds etc. These are required for some of the tests to pass.

To run the full functional test suite against your local bedrock instance, type::

    npm test -- tests/functional --config=tests/config.json

This is just shorthand for the following command::

    PHANTOMJS_EXECUTABLE=./node_modules/.bin/phantomjs ./node_modules/.bin/casperjs test tests/functional --config=tests/config.json

This will run all test suites found in the ``tests/functional`` directory and assumes you
have bedrock running at ``localhost`` on port ``8000``.

To run a single test suite you must tell CasperJS to execute a specific file
e.g. ``tests/functional/home.js``::

    npm test -- tests/functional/home.js --config=tests/config.json

You can also easily run the tests against any bedrock environment by specifying the
``--domain`` variable. For example, to run all functional tests against dev::

    npm test -- tests/functional --domain=https://www-dev.allizom.org --config=tests/config.json

.. Note::

    Passing arguments to ``npm test`` requires at least npm v2.0.0. If you're using an
    older version of npm, you can still run the tests using the full, long verion of the
    command shown above, instead of using the ``npm test`` shortcut.

Writing CasperJS tests
----------------------

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

Debugging CasperJS
------------------

You can enable logging on the command line by passing the following additional flags::

    --verbose --log-level=debug

Guidelines for writing functional tests
---------------------------------------

* Try and keep tests organized and cleanly separated. Each page should have its own test file, and each test should be responsible for a specific purpose, or component of a page.
* Avoid using generic timeouts. Always use CasperJS methods such as ``waitUntilVisible``, ``waitForSelector``, ``waitForUrl`` etc.
* Don't nest callbacks. Try and keep a flat hierarchy for async functions to avoid tests exiting early.
* Don't make tests overly specific. If a test keeps failing because of generic changes to a page such as an image filename or ``href`` being updated, then the test is probably too specific.
* Avoid string checking as tests may break if strings are updated, or could change depending on the page locale.
* If you write something reusable, consider adding it to ``helpers.js`` or ``config.js``.
* When writing tests, try and run them against a staging or demo environment in addition to local testing.

Running Jasmine tests using Karma
---------------------------------

To perform a single run of the Jasmine test suite using Firefox, type the following command::

	grunt test

.. note::

    The Tabzilla tests require that you have your local bedrock development server running on port 8000.

See the `Jasmine`_ documentation for tips on how to write JS behavioral or unit tests.
We also use `Sinon`_ for creating test spies, stubs and mocks.

.. _CasperJS: http://casperjs.org/
.. _CasperJS documentation: http://casperjs.readthedocs.org/en/latest/
.. _PhantomJS: http://phantomjs.org/
.. _PhantomJS 1.9.8: https://bitbucket.org/ariya/phantomjs/downloads
.. _Jasmine: https://jasmine.github.io/1.3/introduction.html
.. _Karma: https://karma-runner.github.io/
.. _Sinon: http://sinonjs.org/
