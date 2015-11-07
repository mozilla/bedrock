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
    $ bin/peep.py install -r requirements/test.txt

Running Jasmine tests using Karma
---------------------------------

To perform a single run of the Jasmine test suite using Firefox, type the
following command:

.. code-block:: bash

    $ grunt test

See the `Jasmine`_ documentation for tips on how to write JS behavioral or unit
tests. We also use `Sinon`_ for creating test spies, stubs and mocks.

Running Selenium tests
----------------------

.. Note::

  Before running the Selenium tests, please make sure to follow the bedrock
  :ref:`installation docs<install>`, including the database sync that is needed
  to pull in external data such as event/blog feeds etc. These are required for
  some of the tests to pass.

To run the full functional test suite against your local bedrock instance:

.. code-block:: bash

    $ py.test --driver Firefox --html tests/functional/results.html -n auto tests/functional/

This will run all test suites found in the ``tests/functional`` directory and
assumes you have bedrock running at ``localhost`` on port ``8000``. Results will
be reported in ``tests/functional/results.html`` and tests will run in parallel
according to the number of cores available.

.. Note::

    For the above command to work, Firefox needs to be installed in a
    predictable location for your operating system. For details on how to
    specify the location of Firefox, or running the tests against alternative
    browsers, refer to the `pytest-selenium documentation`_.

To run a single test file you must tell py.test to execute a specific file
e.g. ``tests/functional/test_newsletter.py``:

.. code-block:: bash

    $ py.test --driver Firefox --html tests/functional/results.html -n auto tests/functional/test_newsletter.py

You can also easily run the tests against any bedrock environment by specifying the
``--base-url`` argument. For example, to run all functional tests against dev:

.. code-block:: bash

    $ py.test --base-url https://www-dev.allizom.org --driver Firefox --html tests/functional/results.html -n auto tests/functional/

For more information on command line options, see the `pytest documentation`_.

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

Sanity tests
~~~~~~~~~~~~

Sanity tests are run as part of bedrocks deployment pipeline. These should be considered
to be critical tests which benefit from being run automatically after every commit to
master. Only the full suite of functional tests are run after deployment to staging. If
your test should be marked as a santity test you will need to apply a ``santiy`` marker
to it.

.. code-block:: python

    import pytest

    @pytest.mark.sanity
    @pytest.mark.nondestructive
    def test_newsletter_default_values(base_url, selenium):
        page = NewsletterPage(base_url, selenium).open()
        assert '' == page.email
        assert 'United States' == page.country
        assert 'English' == page.language
        assert page.html_format_selected
        assert not page.text_format_selected
        assert not page.privacy_policy_accepted

You can run sanity tests only by adding ``-m sanity`` when running the test suite on the
command line.

.. Note::

  Tests that rely on long-running timeouts, cron jobs, or that test for locale specific
  interactions should not be marked as a sanity test. We should try and ensure that the
  suite of sanity tests are quick to run, and they should not have a dependency on
  checking out and building the full site.

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
