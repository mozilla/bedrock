# Front-end testing {: #testing }

Bedrock runs several different types of front-end tests to ensure that the site is working correctly and that new changes don't break existing functionality.

-   [Jasmine](https://jasmine.github.io/index.html) unit/behavioral tests are used to test JavaScript code that runs in the browser. These tests are run against both Firefox and Chrome browsers via a GitHub action, which is triggered against all pull requests and commits to the main branch.
-   [Playwright](https://playwright.dev) integration tests are used to run end-to-end tests in a real browser environment. These tests are run automatically as part of our CI deployment process against dev, stage, and prod. Playwright tests are run against Firefox, Chromium, and Webkit headless browsers for cross-engine coverage.
-   [Axe](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md) tests are used to test for accessibility issues on key pages. These tests are not run as part of our CI deployment process as they can contain a lot of information, but instead run once per day via a GitHub action against dev. Axe tests are run via Playwright as a subset of tests using the `@a11y` tag. Accessibility issues are reported in the GitHub action output, which can be downloaded and reviewed.
-   [Selenium](http://docs.seleniumhq.org/) tests are bedrock's older, legacy integration test suite. These tests now consist only of a small set of smoke tests that are targeted at Internet Explorer 11 (via Sauce Labs) as part of our CI pipeline, and run alongside the Playwright tests.

!!! note
    New integration tests should be written using Playwright. The Selenium Internet Explorer tests continue to run for the time being, but can be retired in the future when the time is right.


The test specs for all of the above suites can be found in the root `./tests` directory:

-   `./tests/unit/` for Jasmine tests.
-   `./tests/playwright/` Playwright tests.
-   `./tests/playwright/specs/a11y/` Axe tests.
-   `./tests/functional/` for Selenium tests.

## Automating the browser

Jasmine, Playwright and Selenium all require a browser to run. In order to automate browsers such as Firefox and Chrome, you may also need to have the appropriate drivers installed. To download `geckodriver` and `chromedriver` and have them ready to run in your system, there are a couple of ways:

Download [geckodriver](https://github.com/mozilla/geckodriver/releases/latest) and add it to your system path:

``` bash
$ cd /path/to/your/downloaded/files/
```

``` bash
$ mv geckodriver /usr/local/bin/
```

If you're on MacOS, download `geckodriver` directly using Homebrew, which automatically places it in your system path:

``` bash
$ brew install geckodriver
```

Download [chromedriver](https://chromedriver.chromium.org/downloads) and add it to your system path:

``` bash
$ cd /path/to/your/downloaded/files/
```

``` bash
$ mv chromedriver /usr/local/bin/
```

If you're on MacOS, download `chromedriver` directly using Homebrew/Cask, which automatically places it in your system path:

``` bash
$ brew tap homebrew/cask
```

``` bash
$ brew cask install chromedriver
```

## Running Jasmine tests

Jasmine and its dependencies are installed via npm and are included when you run `make preflight` to install bedrock's main dependencies.

``` bash
$ make preflight
```

Next, make sure you activate your bedrock virtual env.

``` bash
$ pyenv activate bedrock
```

You can then run the full suite of Jasmine tests with the following command:

``` bash
$ npm run test
```

This will also run all our front-end linters and formatting checks before running the Jasmine test suite. If you only want to run the tests themselves, you can run:

``` bash
$ npm run jasmine
```

### Writing Jasmine tests

See the [Jasmine](https://jasmine.github.io/index.html) documentation for tips on how to write JS behavioral or unit tests. We also use [Sinon](http://sinonjs.org/) for creating test spies, stubs and mocks.

### Debugging Jasmine tests

If you need to debug Jasmine tests, you can also run them interactively in the browser using the following command:

``` bash
$ npm run jasmine-serve
```

## Running Playwright tests

Playwright test dependencies are installed via NPM but are not included in the `make preflight` command along with bedrock's core dependencies. This is because the dependencies are not required to run the site, and also include several large binary files for each headless browser engine.

To install the Playwright dependencies, run the following command:

``` bash
$ cd tests/playwright && npm install && npm run install-deps
```

### Specifying an environment

By default Playwright tests will run against `http://localhost:8000/`. Remember to have your development server running before starting the test suite locally.

You can also set `PLAYWRIGHT_BASE_URL` in your `.env` to point to a different environment, such as dev or stage. For example:

``` bash
PLAYWRIGHT_BASE_URL=https://dev.bedrock.nonprod.webservices.mozgcp.net
```

### Running the test suite

To run the full suite of tests (from the `/tests/playwright/` directory):

``` bash
$ npm run integration-tests
```

This will run all tests against three different headless browser engines (Firefox, Chromium, WebKit).

### Running specific tests

Tests are grouped using tags, such as `@mozorg`, `@firefox`, `@vpn`. To run only one group of tests, instead of the whole suite, you can use `--grep`:

``` bash
$ npx playwright test --grep @firefox
```

To run only a specific test file, such as `firefox-new.spec.js`, you can pass the filename:

``` bash
$ npx playwright test firefox-new
```

See the [Playwright CLI docs](https://playwright.dev/docs/test-cli) for more options when running and debugging tests.

### Writing tests

Playwright test spec files are found in the `./tests/playwright/specs/` directory.

See the Playwright docs for more examples on [how to write tests](https://playwright.dev/docs/writing-tests).

#### Guidelines for writing integration tests

-   Try and keep tests focused on user journeys and key functionality. For example, a test for the download page should focus on the download button, and not the footer or header.
-   Test expected functionality from a **user perspective**. For example, if a user clicks a button, the test should check that the expected action occurs. Try to avoid testing implementation details, as these are both invisible to the user and likely to change more frequently.
-   Keep tests organized and cleanly separated. Each page should have its own test spec file, and each test should be responsible for a specific purpose, or component of a page.
-   Try and use `data-testid` attributes for a [locator strategy](https://playwright.dev/docs/locators#locate-by-test-id), as these are less likely to change than other attributes.
-   Avoid string checking as tests may break if strings are updated, or could change depending on the page locale.
-   When writing tests, push them to the `run-integration-tests` branch to run them against the deployed environment prior to merging to `main`. This will allow you to catch any issues that may not be present in local testing. It's also worth running tests a few times to identify any potential intermittent failures.

### User Agent string overrides

Playwright tests use User Agent string overrides to mock different browser and operating systems combinations. By default tests run with User Agent strings configured for Firefox and Chrome running on Windows, and Safari running on macOS. This is accomplished using an `OpenPage()` helper that can be imported in each test file:

``` javascript
const openPage = require('../scripts/open-page');
const url = '/en-US/products/vpn/';

test.beforeEach(async ({ page, browserName }) => {
    await openPage(url, page, browserName);
});
```

To mock a different browser or operating system combination, tests can manually load a different override instead of using `openPage`:

``` javascript
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
```

## Accessibility testing (Axe)

[Axe](https://github.com/dequelabs/axe-core-npm/blob/develop/packages/playwright/README.md) tests are run as a subset of Playwright tests using the `@a11y` tag. These tests are run against the dev environment once per day via a GitHub action. The axe spec files can be found in the `./tests/playwright/specs/a11y/` directory.

To run the Axe tests locally, you can use the following command from the `./tests/playwright/` directory:

``` bash
$ npm run a11y-tests
```

The Axe tests consist of two different test types. One that scans an entire page for accessibility issues, and another that scans a specific element for issues (such as the main navigation and footer). These tests can also be run at both desktop and mobile viewport sizes.

Test results are output to the console, and any issues found will be created as HTML report files in the `./tests/playwright/test-results-a11y/` directory. When run via the [GitHub action](https://github.com/mozilla/bedrock/actions/workflows/a11y_tests.yml), the reports are also output to the annotation logs for each test job.

A list of all the Axe rules that are checked by the tests can be viewed in the [axe-core repo](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md).

## Running Selenium tests

!!! note
    The majority of Selenium tests have now been migrated to Playwright. We still use Selenium for a small suite of IE focused smoke tests, but most new integration tests should be written using Playwright.


Before running the Selenium tests, please make sure to follow the bedrock `installation docs<install>`{.interpreted-text role="ref"}, including the database sync that is needed to pull in external data such as event/blog feeds etc. These are required for some of the tests to pass.

To run the full Selenium integration test suite against your local bedrock instance:

``` bash
$ pytest --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/
```

This will run all test suites found in the `tests/functional` directory and assumes you have bedrock running at `localhost` on port `8000`. Results will be reported in `tests/functional/results.html`.

!!! note
    If you omit the `--base-url` command line option then a local instance of bedrock will be started, however the tests are not currently able to run against bedrock in this way.


By default, tests will run one at a time. This is the safest way to ensure predictable results, due to [bug 1230105](https://bugzilla.mozilla.org/show_bug.cgi?id=1230105). If you want to run tests in parallel (this should be safe when running against a deployed instance), you can add `-n auto` to the command line. Replace `auto` with an integer if you want to set the maximum number of concurrent processes.

!!! note
    There are some tests that do not require a browser. These can take a long time to run, especially if they're not running in parallel. To skip these tests, add `-m 'not headless'` to your command line.


To run a single test file you must tell pytest to execute a specific file e.g. `tests/functional/firefox/new/test_download.py`:

``` bash
$ pytest --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/firefox/new/test_download.py
```

To run a single test you can filter using the `-k` argument supplied with a keyword e.g. `-k test_download_button_displayed`:

``` bash
$ pytest --base-url http://localhost:8000 --driver Firefox --html tests/functional/results.html tests/functional/firefox/new/test_download.py -k test_download_button_displayed
```

You can also easily run the tests against any bedrock environment by specifying the `--base-url` argument. For example, to run all Selenium integration tests against dev:

``` bash
$ pytest --base-url https://www-dev.allizom.org --driver Firefox --html tests/functional/results.html tests/functional/
```

!!! note
    For the above commands to work, Firefox needs to be installed in a predictable location for your operating system. For details on how to specify the location of Firefox, or running the tests against alternative browsers, refer to the [pytest-selenium documentation](http://pytest-selenium.readthedocs.org/en/latest/index.html).


For more information on command line options, see the [pytest documentation](http://pytest.org/latest/).

### Running tests in Sauce Labs

You can also run tests in Sauce Labs directly from the command line. This can be useful if you want to run tests against Internet Explorer when you're on Mac OSX, for instance.

1.  Sign up for an account at <https://saucelabs.com/opensauce/>.
2.  Log in and obtain your Remote Access Key from user settings.
3.  Run a test specifying `SauceLabs` as your driver, and pass your credentials.

For example, to run the home page tests using Internet Explorer via Sauce Labs:

``` bash
$ SAUCELABS_USERNAME=thedude SAUCELABS_API_KEY=123456789 SAUCELABS_W3C=true SELENIUM_EXCLUDE_DEBUG=logs pytest --base-url https://www-dev.allizom.org --driver SauceLabs --capability browserName 'internet explorer' --capability platformName 'Windows 10' --html tests/functional/results.html tests/functional/test_home.py
```

### Writing Selenium tests

Tests usually consist of interactions and assertions. Selenium provides an API for opening pages, locating elements, interacting with elements, and obtaining state of pages and elements. To improve readability and maintainability of the tests, we use the [Page Object](http://martinfowler.com/bliki/PageObject.html) model, which means each page we test has an object that represents the actions and states that are needed for testing.

Well written page objects should allow your test to contain simple interactions and assertions as shown in the following example:

``` python
def test_sign_up_for_newsletter(base_url, selenium):
    page = NewsletterPage(base_url, selenium).open()
    page.type_email("noreply@mozilla.com")
    page.accept_privacy_policy()
    page.click_sign_me_up()
    assert page.sign_up_successful
```

It's important to keep assertions in your tests and not your page objects, and to limit the amount of logic in your page objects. This will ensure your tests all start with a known state, and any deviations from this expected state will be highlighted as potential regressions. Ideally, when tests break due to a change in bedrock, only the page objects will need updating. This can often be due to an element needing to be located in a different way.

Please take some time to read over the [Selenium documentation](http://seleniumhq.github.io/selenium/docs/api/py/api.html) for details on the Python client API.

#### Destructive tests

By default all tests are assumed to be destructive, which means they will be skipped if they're run against a [sensitive environment](http://pytest-selenium.readthedocs.org/en/latest/user_guide.html#sensitive-environments). This prevents accidentally running tests that create, modify, or delete data on the application under test. If your test is nondestructive you will need to apply the `nondestructive` marker to it. A simple example is shown below, however you can also read the [pytest markers](http://pytest.org/latest/example/markers.html) documentation for more options.

``` python
import pytest


@pytest.mark.nondestructive
def test_newsletter_default_values(base_url, selenium):
    page = NewsletterPage(base_url, selenium).open()
    assert "" == page.email
    assert "United States" == page.country
    assert "English" == page.language
    assert page.html_format_selected
    assert not page.text_format_selected
    assert not page.privacy_policy_accepted
```

#### Smoke tests

Smoke tests are considered to be our most critical tests that must pass in a wide range of web browsers, including Internet Explorer 11. The number of smoke tests we run should be enough to cover our most critical pages where legacy browser support is important.

``` python
import pytest


@pytest.mark.smoke
@pytest.mark.nondestructive
def test_firefox_menu_displayed(base_url, selenium):
    page = HomePage(selenium, base_url, params="").open()
    assert page.navigation.is_firefox_menu_displayed
```

You can run smoke tests only by adding `-m smoke` when running the test suite on the command line.

#### Waits and Expected Conditions

Often an interaction with a page will cause a visible response. While Selenium does its best to wait for any page loads to be complete, it's never going to be as good as you at knowing when to allow the test to continue. For this reason, you will need to write explicit [waits](http://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.wait.html) in your page objects. These repeatedly execute code (a condition) until the condition returns true. The following example is probably the most commonly used, and will wait until an element is considered displayed:

``` python
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.ui import WebDriverWait as Wait

Wait(selenium, timeout=10).until(
    expected.visibility_of_element_located(By.ID, "my_element")
)
```

For convenience, the Selenium project offers some basic [expected conditions](http://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html), which can be used for the most common cases.

### Debugging Selenium

Debug information is collected on failure and added to the HTML report referenced by the `--html` argument. You can enable debug information for all tests by setting the `SELENIUM_CAPTURE_DEBUG` environment variable to `always`.

## Testing Basket email forms

When writing integration tests for front-end email newsletter forms that submit to [Basket](https://github.com/mozilla/basket), we have some special case email addresses that can be used just for testing:

1.  Any newsletter subscription request using the email address "success@example.com" will always return success from the basket client.
2.  Any newsletter subscription request using the email address "failure@example.com" will always raise an exception from the basket client.

Using the above email addresses enables newsletter form testing without actually hitting the Basket instance, which reduces automated newsletter spam and improves test reliability due to any potential network flakiness.

### Headless tests

There are targeted headless tests for the [download](https://github.com/mozilla/bedrock/blob/main/tests/functional/test_download.py) pages. These tests and are run as part of the pipeline to ensure that download links constructed via product details are well formed and return valid 200 responses.
