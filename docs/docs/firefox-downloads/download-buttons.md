---
render_macros: true
---

To ensure that visitors to Firefox download pages get served the correct build and installer type for their operating system, we rely on [User Agent](https://developer.mozilla.org/docs/Glossary/User_agent) information to figure out what's needed. We primarily use the [Client Hints API](https://developer.mozilla.org/docs/Web/HTTP/Guides/Client_hints) to query this information, falling back to [navigator.UserAgent](https://developer.mozilla.org/docs/Web/API/Navigator/userAgent) for other web browsers.

The logic for this User Agent detection can be found in `/media/js/base/site.js`. The script adds a computed platform based CSS class name such as `windows`, `osx`, `linux`, `android` or `ios` to the root `<html>` element of the DOM. This class is then used as a styling hook for displaying platform specific content, such as the correct download button to display. The CSS selectors that are specific to Firefox download buttons can be found in `media/css/protocol/components/_download-button.scss`, which are imported into the global site base stylesheet.

The `site.js` script gets loaded in the `<head>` of each page. This is important to ensure a fast contentful first paint and to avoid flashes of conditional content, but also means it is equally important to ensure that `site.js` remains small and fast since it is render blocking. Use your judgement here wisely and run performance tests when making changes.

Web browser vendors are also starting to freeze and limit the types information contained in User Agent strings today, so a good rule of thumb is to only rely on very basic information whenever possible, such as operating system name. Changes to the logic in `site.js` have potential to have site wide impact, so they must be made carefully and with a good amount of QA and testing. There are also tests in `tests/unit/spec/base/site.js`, so please maintain these and keep adding to them for your own sanity. The Playwright integration tests should also hopefully pick up possible regressions that might impact user flows.

# Helpers

There are two Firefox download button helpers in bedrock to choose from. The first is a lightweight button that links directly to the `/firefox/download/thanks/` page. Its sole purpose is to facilitate downloading the main release version of Firefox.

``` jinja
{{ download_firefox_thanks() }}
```

The download button rendered by the `download_firefox_thanks()` helper is identical for all supported operating systems. The rendered button links to the `/firefox/download/thanks/` page, which is a single destination for the majority of release-channel download buttons on the website. The `/thanks/` page contains all the JS logic to figure out the correct build and trigger a file download automatically when the page loads. That logic can be found in `media/js/firefox/new/common/thanks.js`.

The second type of button is more heavyweight, and can be configured to download any build of Firefox (e.g. Release, Beta, Developer Edition, Nightly). It can also offer functionality such as direct (in-page) download links and different installer types, so it comes with a lot more complexity.

``` jinja
{{ download_firefox() }}
```

The download button rendered by the `download_firefox()` helper is actually several different download buttons all folded into one. Each button is for a different build or operating system supported by Firefox. Only one button is displayed to the visitor at any one time, using the logic in `site.js` and `_download-button.scss` to determine which one is correct. For users with JS disabled, they see a list of all download options. Because this button is a lot more complex, it should be tested very carefully when making changes or adding new builds.

## Which helper should I use?

A good rule of thumb is to always use `download_firefox_thanks()` for regular landing pages (such as `/firefox/new/`) where the main release version of Firefox is the product being offered. For pages pages that require direct download links, or promote pre-release products (such as `/firefox/channel/`) then `download_firefox()` should be used instead.

## A note for future brave developers

Much of the logic in the `{{ download_firefox() }}` helper is OLD, and could be refactored. It could be nice, for example, to move all of the logic for determining the right build of Firefox entirely into JS where it is easier to write tests for, eliminating the delicate selector classes in `_download-button.scss`. We made inroads to doing this with the lightweight `download_firefox_thanks()` helper (see above) that points to `/firefox/download/thanks/`, but the more heavyweight `download_firefox()` helper still relies on `_download-button.scss` to display the correct download links. We'd still need to maintain a no-JS fallback, but this could be as simple as a link to `/firefox/all/`.

## Documentation

See [helpers.py](https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/templatetags/helpers.py) for documentation and supported parameters for both buttons.

