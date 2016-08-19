.. This Source Code Form is subject to the terms of the Mozilla Public
.. License, v. 2.0. If a copy of the MPL was not distributed with this
.. file, You can obtain one at http://mozilla.org/MPL/2.0/.

.. _testing:

=================
Front-end testing
=================

Bedrock runs a suite of front-end `Jasmine`_ behavioral/unit tests, which use
`Karma`_ as a test runner. We also have a suite of functional tests using
`Selenium`_ and `pytest`_. This allows us to emulate users interacting with a
real browser. All these test suites live in the ``tests`` directory.

The ``tests`` directory comprises of:

* ``/functional`` contains pytest tests.
* ``/pages`` contains Python page objects.
* ``/unit`` contains the Jasmine tests and Karma config file.

Installation
------------

First follow the :ref:`installation instructions for bedrock<install>`, which
will install the specific versions of Jasmine/Karma which are needed to run the
unit tests, and guide you through installing pip and setting up a virtual
environment for the functional tests. The additional requirements can then be
installed by using the following commands:

.. code-block:: bash

    $ source venv/bin/activate
    $ pip install -r requirements/test.txt

Running Jasmine tests using Karma
---------------------------------

To perform a single run of the Jasmine test suite using Firefox, type the
following command:

.. code-block:: bash

    $ gulp js:test

See the `Jasmine`_ documentation for tips on how to write JS behavioral or unit
tests. We also use `Sinon`_ for creating test spies, stubs and mocks.

Running functional tests
------------------------

.. Note::

  Before running the functional tests, please make sure to follow the bedrock
  :ref:`installation docs<install>`, including the database sync that is needed
  to pull in external data such as event/blog feeds etc. These are required for
  some of the tests to pass. To run the tests using Firefox, you must also first
  download `geckodriver`_ and make it available in your `system path`_. You can
  alternatively specify the path to geckodriver using the command line (see the
  `pytest-selenium documentation`_ for more information).

To run the full functional test suite against your local bedrock instance:

.. code-block:: bash

    $ py.test --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/

This will run all test suites found in the ``tests/functional`` directory and
assumes you have bedrock running at ``localhost`` on port ``8000``. Results will
be reported in ``tests/functional/results.html``.

.. Note::

    If you omit the ``--base-url`` command line option then a local instance of
    bedrock will be started, however the tests are not currently able to run
    against bedrock in this way.

By default, tests will run one at a time. This is the safest way to ensure
predictable results, due to
`bug 1230105 <https://bugzilla.mozilla.org/show_bug.cgi?id=1230105>`_.
If you want to run tests in parallel (this should be safe when running against
a deployed instance), you can add ``-n auto`` to the command line. Replace
``auto`` with an integer if you want to set the maximum number of concurrent
processes.

.. Note::

    There are some functional tests that do not require a browser. These can
    take a long time to run, especially if they're not running in parallel.
    To skip these tests, add ``-m 'not headless'`` to your command line.

To run a single test file you must tell py.test to execute a specific file
e.g. ``tests/functional/test_newsletter.py``:

.. code-block:: bash

    $ py.test --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/test_newsletter.py

To run a single test you can filter using the ``-k`` argument supplied with a keyword
e.g. ``-k test_successful_sign_up``:

.. code-block:: bash

  $ py.test --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/test_newsletter.py -k test_successful_sign_up

You can also easily run the tests against any bedrock environment by specifying the
``--base-url`` argument. For example, to run all functional tests against dev:

.. code-block:: bash

    $ py.test --base-url https://www-dev.allizom.org --driver Firefox --html tests/functional/results.html tests/functional/

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

    $ SAUCELABS_USERNAME=thedude SAUCELABS_API_KEY=123456789 py.test --base-url https://www-dev.allizom.org --driver SauceLabs --capability browserName 'internet explorer' -n auto --html tests/functional/results.html tests/functional/test_home.py


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

.. _smoke-functional-tests:

Smoke tests
~~~~~~~~~~~

Smoke tests are run on every commit to master as part of bedrocks deployment pipeline.
These should be considered as critical baseline functional tests. (Note: we only run the
full suite of cross-browser functional tests on tagged commits. See :ref:`tagged-commit`).
If your test should be considered a smoke test you will need to apply a ``smoke`` marker
to it.

.. code-block:: python

    import pytest

    @pytest.mark.smoke
    @pytest.mark.nondestructive
    def test_newsletter_default_values(base_url, selenium):
        page = NewsletterPage(base_url, selenium).open()
        assert '' == page.email
        assert 'United States' == page.country
        assert 'English' == page.language
        assert page.html_format_selected
        assert not page.text_format_selected
        assert not page.privacy_policy_accepted

You can run smoke tests only by adding ``-m smoke`` when running the test suite on the
command line.

.. Note::

  Tests that rely on long-running timeouts, cron jobs, or that test for locale specific
  interactions should not be marked as a smoke test. We should try and ensure that the
  suite of smoke tests are quick to run, and they should not have a dependency on
  checking out and building the full site.

Sanity tests
~~~~~~~~~~~~

Sanity tests are considered to be our most critical tests that must pass in a wide range
of web browsers, including old versions of Internet Explorer. Sanity tests are run
automatically post deployment on a wider range of browsers & platforms than we run the
full suite against. The number of sanity tests we run should remain small, but cover our
most critical pages where legacy browser support is important. Sanity tests are typically
run after a tagged commit to master (see :ref:`tagged-commit`).

.. code-block:: python

    import pytest

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_click_download_button(base_url, selenium):
        page = FirefoxNewPage(base_url, selenium).open()
        page.download_firefox()
        assert page.is_thank_you_message_displayed

You can run sanity tests only by adding ``-m sanity`` when running the test suite on the
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

Guidelines for writing functional tests
---------------------------------------

* Try and keep tests organized and cleanly separated. Each page should have its
  own page object and test file, and each test should be responsible for a
  specific purpose, or component of a page.
* Avoid using sleeps - always use waits as mentioned above.
* Don't make tests overly specific. If a test keeps failing because of generic
  changes to a page such as an image filename or ``href`` being updated, then
  the test is probably too specific.
* Avoid string checking as tests may break if strings are updated, or could
  change depending on the page locale.
* When writing tests, try and run them against a staging or demo environment
  in addition to local testing. It's also worth running tests a few times to
  identify any intermittent failures that may need additional waits.

See also the `Web QA style guide`_ for Python based testing.

Testing Basket email forms
--------------------------

When writing functional tests for front-end email newsletter forms that submit to
`Basket`_, we have some special case email addresses that can be used just for testing:

#. Any newsletter subscription request using the email address "success@example.com"
   will always return success from the basket client.
#. Any newsletter subscription request using the email address "failure@example.com"
   will always raise an exception from the basket client.

Using the above email addresses enables newsletter form testing without actually hitting
the Basket instance, which reduces automated newsletter spam and improves test
reliability due to any potential network flakiness.

Link Checks
-----------

A full link checker is run over the production environments, which uses a tool named
`LinkChecker`_ to crawl the entire website and reports any broken or malformed links both
internally and externally. These jobs are run once a day in the `Jenkins instance`_ and
are named with the ``bedrock_linkchecker_`` prefix.

In addition, there are targeted functional tests for the `download`_ and `localized
download`_ pages. These tests do not use the LinkChecker tool, and are run as part of
the pipeline, which ensures that any broken download links are noticed much earlier,
and also do not depend on a crawler to find them.

.. _Jasmine: https://jasmine.github.io/1.3/introduction.html
.. _Karma: https://karma-runner.github.io/
.. _Sinon: http://sinonjs.org/
.. _Selenium: http://docs.seleniumhq.org/
.. _pytest: http://pytest.org/latest/
.. _pytest documentation: http://pytest.org/latest/
.. _pytest markers: http://pytest.org/latest/example/markers.html
.. _pytest-selenium documentation: http://pytest-selenium.readthedocs.org/en/latest/index.html
.. _sensitive environment: http://pytest-selenium.readthedocs.org/en/latest/user_guide.html#sensitive-environments
.. _Selenium documentation: http://seleniumhq.github.io/selenium/docs/api/py/api.html
.. _Page Object: http://martinfowler.com/bliki/PageObject.html
.. _waits: http://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.wait.html
.. _expected conditions: http://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html
.. _Web QA style guide: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide
.. _LinkChecker: http://wummel.github.io/linkchecker/
.. _Jenkins instance: https://ci.us-west.moz.works/
.. _download: https://github.com/mozilla/bedrock/blob/master/tests/functional/test_download.py
.. _localized download: https://github.com/mozilla/bedrock/blob/master/tests/functional/test_download_l10n.py
.. _Basket: https://github.com/mozilla/basket
.. _geckodriver: https://github.com/mozilla/geckodriver/releases/latest
.. _system path: https://developer.mozilla.org/docs/Mozilla/QA/Marionette/WebDriver#Add_executable_to_system_path
