.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at https://mozilla.org/MPL/2.0/.

.. _testing:

=================
Front-end testing
=================

Bedrock runs several different types of front-end tests to ensure that the site is working
correctly and that new changes don't break existing functionality.

- `Jasmine`_ unit/behavioral tests are used to test JavaScript code that runs in the browser.
  These tests are run against both Firefox and Chrome browsers via a GitHub action, which is
  triggered against all pull requests and commits to the main branch.
- `Playwright`_ integration tests are used to run end-to-end tests in a real browser
  environment. These tests are run automatically as part of our CI deployment process against
  dev, stage, and prod. Playwright tests are run against Firefox, Chromium, and Webkit headless
  browsers for cross-engine coverage.
- `Selenium`_ tests are bedrock's older, legacy integration test suite, which will eventually be
  replaced by Playwright. These tests are run against Firefox, Chrome, and Internet Explorer
  (via a mix of both a local Selenium Grid and Sauce Labs) as part of our CI pipeline, and
  run alongside the Playwright tests.

.. note::

  New integration tests should be written using Playwright, but we will continue to run the
  Selenium tests until they are all migrated over. We will also eventually retire the
  Internet Explorer tests.

The test specs for all of the above suites can be found in the root ``./tests`` directory:

* ``./tests/unit/`` for Jasmine tests.
* ``./tests/playwright/`` Playwright tests.
* ``./tests/functional/`` for Selenium tests.

Automating the browser
======================

Jasmine, Playwright and Selenium all require a browser to run. In order to automate browsers
such as Firefox and Chrome, you may also need to have the appropriate drivers installed. To
download ``geckodriver`` and ``chromedriver`` and have them ready to run in your system,
there are a couple of ways:

Download `geckodriver`_ and add it to your system path:

.. code-block:: bash

    $ cd /path/to/your/downloaded/files/

.. code-block:: bash

    $ mv geckodriver /usr/local/bin/

If you're on MacOS, download ``geckodriver`` directly using Homebrew, which automatically
places it in your system path:

.. code-block:: bash

    $ brew install geckodriver

Download `chromedriver`_ and add it to your system path:

.. code-block:: bash

    $ cd /path/to/your/downloaded/files/

.. code-block:: bash

    $ mv chromedriver /usr/local/bin/

If you're on MacOS, download ``chromedriver`` directly using Homebrew/Cask, which
automatically places it in your system path:

.. code-block:: bash

    $ brew tap homebrew/cask

.. code-block:: bash

    $ brew cask install chromedriver

Running Jasmine tests
=====================

Jasmine and its dependencies are installed via npm and are included when you run
``make preflight`` to install bedrock's main dependencies.

.. code-block:: bash

    $ make preflight

Next, make sure you activate your bedrock virtual env.

.. code-block:: bash

    $ pyenv activate bedrock

You can then run the full suite of Jasmine tests with the following command:

.. code-block:: bash

    $ npm run test

This will also run all our front-end linters and formatting checks before running
the Jasmine test suite. If you only want to run the tests themselves, you can
run:

.. code-block:: bash

    $ npm run jasmine

Writing Jasmine tests
---------------------

See the `Jasmine`_ documentation for tips on how to write JS behavioral or unit
tests. We also use `Sinon`_ for creating test spies, stubs and mocks.

Debugging Jasmine tests
-----------------------

If you need to debug Jasmine tests, you can also run them interactively in the
browser using the following command:

.. code-block:: bash

    $ npm run jasmine-serve

Running Playwright tests
========================

Playwright test dependencies are installed via NPM but are not included in the
``make preflight`` command along with bedrock's core dependencies. This is because
the dependencies are not required to run the site, and also include several large
binary files for each headless browser engine.

To install the Playwright dependencies, run the following command:

.. code-block:: bash

    $ cd tests/playwright && npm install && npm run install-deps

Specifying an environment
-------------------------

By default Playwright tests will run against ``http://localhost:8000/``. Remember
to have your development server running before starting the test suite locally.

You can also set ``PLAYWRIGHT_BASE_URL`` in your ``.env`` to point to a different
environment, such as dev or stage. For example:

.. code-block:: bash

    PLAYWRIGHT_BASE_URL=https://dev.bedrock.nonprod.webservices.mozgcp.net


Running the test suite
----------------------

To run the full suite of tests (from the ``/tests/playwright/`` directory):

.. code-block:: bash

    $ npx playwright test

This will run all tests against three different headless browser engines (Firefox,
Chromium, WebKit).

Running specific tests
----------------------

Tests are grouped using tags, such as ``@mozorg``, ``@firefox``, ``@vpn``. To run
only one group of tests, instead of the whole suite, you can use ``--grep``:

.. code-block:: bash

    $ npx playwright test --grep @firefox

To run only a specific test file, such as ``firefox-new.spec.js``,
you can pass the filename:

.. code-block:: bash

    $ npx playwright test firefox-new

See the `Playwright CLI docs`_ for more options when running and debugging tests.

Writing tests
-------------

Playwright test spec files are found in the ``./tests/playwright/specs/`` directory.

See the Playwright docs for more examples on `how to write tests`_.

Guidelines for writing integration tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Try and keep tests focused on user journeys and key functionality. For example,
  a test for the download page should focus on the download button, and not the
  footer or header.
* Test expected functionality from a **user perspective**. For example, if a user
  clicks a button, the test should check that the expected action occurs. Try
  to avoid testing implementation details, as these are both invisible to the
  user and likely to change more frequently.
* Keep tests organized and cleanly separated. Each page should have its own test
  spec file, and each test should be responsible for a specific purpose, or
  component of a page.
* Try and use ``data-testid`` attributes for a `locator strategy`_, as these are
  less likely to change than other attributes.
* Avoid string checking as tests may break if strings are updated, or could
  change depending on the page locale.
* When writing tests, push them to the ``run-integration-tests`` branch to run
  them against the deployed environment prior to merging to ``main``. This will
  allow you to catch any issues that may not be present in local testing. It's
  also worth running tests a few times to identify any potential intermittent
  failures.

User Agent string overrides
---------------------------

Playwright tests use User Agent string overrides to mock different browser and
operating systems combinations. By default tests run with User Agent strings
configured for Firefox and Chrome running on Windows, and Safari running on
macOS. This is accomplished using an ``OpenPage()`` helper that can be imported
in each test file:

.. code-block:: javascript

    const openPage = require('../scripts/open-page');
    const url = '/en-US/firefox/new/';

    test.beforeEach(async ({ page, browserName }) => {
        await openPage(url, page, browserName);
    });


To mock a different browser or operating system combination, tests can manually
load a different override instead of using ``openPage``:

.. code-block:: javascript

    test.beforeEach(async ({ page, browserName }) => {
        if (browserName === 'webkit') {
            // Set macOS 10.14 UA strings.
            await page.addInitScript({
                path: `./scripts/useragent/mac-old/${browserName}.js`
            });
        } else {
            // Set Windows 8.1 UA strings (64-bit).
            await page.addInitScript({
                path: `./scripts/useragent/win-old/${browserName}.js`
            });
        }

        await page.goto(url + '?automation=true');
    });

Running Selenium tests
======================

.. note::

  Selenium tests are being retired in favour of the newer Playwright test suite.
  Whilst we will continue to run the Selenium tests until they are all migrated
  over, new tests should be written using Playwright.

Before running the Selenium tests, please make sure to follow the bedrock
:ref:`installation docs<install>`, including the database sync that is needed
to pull in external data such as event/blog feeds etc. These are required for
some of the tests to pass.

To run the full Selenium integration test suite against your local bedrock
instance in Mozorg mode:

.. code-block:: bash

    $ pytest --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/

This will run all test suites found in the ``tests/functional`` directory and
assumes you have bedrock running at ``localhost`` on port ``8000``. Results will
be reported in ``tests/functional/results.html``.

To run the full Selenium test suite against your local bedrock instance in
Pocket mode, things are slightly different, because of the way things are set
up in order to allow CI to test both Mozorg Mode and Pocket Mode at the same
time. You need to define a temporary environment variable (needed by the
`pocket_base_url` fixture) and scope pytest to only run Pocket tests:

.. code-block:: bash

    $ BASE_POCKET_URL=http://localhost:8000 pytest -m pocket_mode --driver Firefox --html tests/functional/results.html tests/functional/

This will run all test suites found in the ``tests/functional`` directory that have
the pytest "`mark`" of `pocket_mode` and assumes you have bedrock running *in Pocket mode* at
``localhost`` on port ``8000``. Results will be reported in ``tests/functional/results.html``.

.. Note::

    If you omit the ``--base-url`` command line option in Mozorg mode (ie, not
    in Pocket mode) then a local instance of bedrock will be started, however
    the tests are not currently able to run against bedrock in this way.

By default, tests will run one at a time. This is the safest way to ensure
predictable results, due to
`bug 1230105 <https://bugzilla.mozilla.org/show_bug.cgi?id=1230105>`_.
If you want to run tests in parallel (this should be safe when running against
a deployed instance), you can add ``-n auto`` to the command line. Replace
``auto`` with an integer if you want to set the maximum number of concurrent
processes.

.. Note::

    There are some tests that do not require a browser. These can take a long
    time to run, especially if they're not running in parallel. To skip these
    tests, add ``-m 'not headless'`` to your command line.

To run a single test file you must tell pytest to execute a specific file
e.g. ``tests/functional/test_newsletter.py``:

.. code-block:: bash

    $ pytest --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/firefox/new/test_download.py

To run a single test you can filter using the ``-k`` argument supplied with a keyword
e.g. ``-k test_download_button_displayed``:

.. code-block:: bash

  $ pytest --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/firefox/new/test_download.py -k test_download_button_displayed

You can also easily run the tests against any bedrock environment by specifying the
``--base-url`` argument. For example, to run all Selenium integration tests against
dev:

.. code-block:: bash

    $ pytest --base-url https://www-dev.allizom.org --driver Firefox --html tests/functional/results.html tests/functional/

.. Note::

    For the above commands to work, Firefox needs to be installed in a
    predictable location for your operating system. For details on how to
    specify the location of Firefox, or running the tests against alternative
    browsers, refer to the `pytest-selenium documentation`_.

For more information on command line options, see the `pytest documentation`_.

Running tests in Sauce Labs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also run tests in Sauce Labs directly from the command line. This can be useful
if you want to run tests against Internet Explorer when you're on Mac OSX, for instance.

#. Sign up for an account at https://saucelabs.com/opensauce/.
#. Log in and obtain your Remote Access Key from user settings.
#. Run a test specifying ``SauceLabs`` as your driver, and pass your credentials.

For example, to run the home page tests using Internet Explorer via Sauce Labs:

.. code-block:: bash

    $ SAUCELABS_USERNAME=thedude SAUCELABS_API_KEY=123456789 SAUCELABS_W3C=true SELENIUM_EXCLUDE_DEBUG=logs pytest --base-url https://www-dev.allizom.org --driver SauceLabs --capability browserName 'internet explorer' --capability platformName 'Windows 10' --html tests/functional/results.html tests/functional/test_home.py


Writing Selenium tests
----------------------

Tests usually consist of interactions and assertions. Selenium provides an API
for opening pages, locating elements, interacting with elements, and obtaining
state of pages and elements. To improve readability and maintainability of the
tests, we use the `Page Object`_ model, which means each page we test has an
object that represents the actions and states that are needed for testing.

Well written page objects should allow your test to contain simple interactions
and assertions as shown in the following example:

.. code-block:: python

    def test_sign_up_for_newsletter(base_url, selenium):
        page = NewsletterPage(base_url, selenium).open()
        page.type_email('noreply@mozilla.com')
        page.accept_privacy_policy()
        page.click_sign_me_up()
        assert page.sign_up_successful

It's important to keep assertions in your tests and not your page objects, and
to limit the amount of logic in your page objects. This will ensure your tests
all start with a known state, and any deviations from this expected state will
be highlighted as potential regressions. Ideally, when tests break due to a
change in bedrock, only the page objects will need updating. This can often be
due to an element needing to be located in a different way.

Please take some time to read over the `Selenium documentation`_ for details on
the Python client API.

Destructive tests
~~~~~~~~~~~~~~~~~

By default all tests are assumed to be destructive, which means they will be
skipped if they're run against a `sensitive environment`_. This prevents
accidentally running tests that create, modify, or delete data on the
application under test. If your test is nondestructive you will need to apply
the ``nondestructive`` marker to it. A simple example is shown below, however
you can also read the `pytest markers`_ documentation for more options.

.. code-block:: python

    import pytest

    @pytest.mark.nondestructive
    def test_newsletter_default_values(base_url, selenium):
        page = NewsletterPage(base_url, selenium).open()
        assert '' == page.email
        assert 'United States' == page.country
        assert 'English' == page.language
        assert page.html_format_selected
        assert not page.text_format_selected
        assert not page.privacy_policy_accepted

Smoke tests
~~~~~~~~~~~

Smoke tests are considered to be our most critical tests that must pass in a wide range
of web browsers, including Internet Explorer 11. The number of smoke tests we run should
be enough to cover our most critical pages where legacy browser support is important.

.. code-block:: python

    import pytest

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_download_button_displayed(base_url, selenium):
        page = DownloadPage(selenium, base_url, params='').open()
        assert page.is_download_button_displayed

You can run smoke tests only by adding ``-m smoke`` when running the test suite on the
command line.

Waits and Expected Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Often an interaction with a page will cause a visible response. While Selenium
does its best to wait for any page loads to be complete, it's never going to be
as good as you at knowing when to allow the test to continue. For this reason,
you will need to write explicit `waits`_ in your page objects. These repeatedly
execute code (a condition) until the condition returns true. The following
example is probably the most commonly used, and will wait until an element is
considered displayed:

.. code-block:: python

    from selenium.webdriver.support import expected_conditions as expected
    from selenium.webdriver.support.ui import WebDriverWait as Wait

    Wait(selenium, timeout=10).until(
        expected.visibility_of_element_located(By.ID, 'my_element'))

For convenience, the Selenium project offers some basic `expected conditions`_,
which can be used for the most common cases.

Debugging Selenium
------------------

Debug information is collected on failure and added to the HTML report
referenced by the ``--html`` argument. You can enable debug information for all
tests by setting the ``SELENIUM_CAPTURE_DEBUG`` environment variable to
``always``.

Testing Basket email forms
==========================

When writing integration tests for front-end email newsletter forms that submit to
`Basket`_, we have some special case email addresses that can be used just for testing:

#. Any newsletter subscription request using the email address "success@example.com"
   will always return success from the basket client.
#. Any newsletter subscription request using the email address "failure@example.com"
   will always raise an exception from the basket client.

Using the above email addresses enables newsletter form testing without actually hitting
the Basket instance, which reduces automated newsletter spam and improves test
reliability due to any potential network flakiness.

Headless tests
--------------

There are targeted headless tests for the `download`_ pages.
These tests and are run as part of the pipeline to ensure that download links constructed
via product details are well formed and return valid 200 responses.

.. _Jasmine: https://jasmine.github.io/index.html
.. _Sinon: http://sinonjs.org/
.. _Selenium: http://docs.seleniumhq.org/
.. _pytest documentation: http://pytest.org/latest/
.. _pytest markers: http://pytest.org/latest/example/markers.html
.. _pytest-selenium documentation: http://pytest-selenium.readthedocs.org/en/latest/index.html
.. _sensitive environment: http://pytest-selenium.readthedocs.org/en/latest/user_guide.html#sensitive-environments
.. _Selenium documentation: http://seleniumhq.github.io/selenium/docs/api/py/api.html
.. _Page Object: http://martinfowler.com/bliki/PageObject.html
.. _waits: http://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.wait.html
.. _expected conditions: http://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
.. _download: https://github.com/mozilla/bedrock/blob/main/tests/functional/test_download.py
.. _Basket: https://github.com/mozilla/basket
.. _geckodriver: https://github.com/mozilla/geckodriver/releases/latest
.. _chromedriver: https://chromedriver.chromium.org/downloads
.. _Playwright: https://playwright.dev
.. _Playwright CLI docs: https://playwright.dev/docs/test-cli
.. _how to write tests: https://playwright.dev/docs/writing-tests
.. _locator strategy: https://playwright.dev/docs/locators#locate-by-test-id
