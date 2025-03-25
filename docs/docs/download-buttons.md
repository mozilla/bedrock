---
render_macros: true
---

# Firefox Download Buttons {: #download-buttons }

There are two Firefox download button helpers in bedrock to choose from. The first is a lightweight button that links directly to the `/firefox/download/thanks/` page. Its sole purpose is to facilitate downloading the main release version of Firefox.

``` jinja
{{ download_firefox_thanks() }}
```

The second type of button is more heavy weight, and can be configured to download any build of Firefox (e.g. Release, Beta, Developer Edition, Nightly). It can also offer functionality such as direct (in-page) download links, so it comes with a lot more complexity and in-page markup.

``` jinja
{{ download_firefox() }}
```

## Which button should I use?

A good rule of thumb is to always use `download_firefox_thanks()` for regular landing pages (such as `/firefox/new/`) where the main release version of Firefox is the product being offered. For pages pages that require direct download links, or promote pre-release products (such as `/firefox/channel/`) then `download_firefox()` should be used instead.

## Documentation

See [helpers.py](https://github.com/mozilla/bedrock/blob/main/bedrock/firefox/templatetags/helpers.py) for documentation and supported parameters for both buttons.
