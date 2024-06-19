# Playwright integration tests

See the [Playwright documentation](https://playwright.dev/docs/intro)
for detailed information on how to write, run and debug tests.

## Installation

Install Playwright and headless browser engines:

```
npm install && npm run install-deps
```

## Specifying an environment

By default tests will run against `http://localhost:8000/`.
You can set `PLAYWRIGHT_BASE_URL` in your `.env` to point to
a different environment. Remember to have your development
server running before starting the test suite locally.

## Running the test suite

To run the full suite of tests:

```
npx playwright test
```

This will run all tests against three different headless browser
engines (Firefox, Chromium, WebKit).

### Running specific tests

Tests are grouped using tags, such as `@mozorg`, `@firefox`, `@vpn`.
To run only one group of tests, instead of the whole suite, you
can use `--grep`:

```
npx playwright test --grep @firefox
```

To run only a specific test file, such as `firefox-new.spec.js`,
you can pass the filename:

```
npx playwright test firefox-new
```

See the [Playwright CLI docs](https://playwright.dev/docs/test-cli)
for more options when running and debugging tests.

### Writing tests

Test spec files are found in the `./tests/playwright/specs/`
directory. See the Playwright docs for more examples on [how
to write tests](https://playwright.dev/docs/writing-tests).

#### Specifying browsers and operating systems.

Tests use User Agent string overrides to mock different browser
and operating systems combinations. By default tests run with
User Agent strings configured for Firefox and Chrome running
on Windows 10, and Safari running on macOS 10.15.7. This is
accomplished using an `OpenPage()` helper that can be imported
in each test file:

```javascript
const openPage = require('../scripts/open-page');
const url = '/en-US/firefox/new/';

test.beforeEach(async ({ page, browserName }) => {
    await openPage(url, page, browserName);
});
```

To mock a different browser or operating system combination,
tests can manually load a different override instead of using
`openPage`:

```javascript
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
