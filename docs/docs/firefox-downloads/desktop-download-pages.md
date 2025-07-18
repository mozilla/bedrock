---
render_macros: true
---

What we typically refer to as the "download page" is [https://www.firefox.com/en-US/](https://www.firefox.com/en-US/) the request for that url is handled by the [DownloadView](https://github.com/mozmeao/springfield/blob/5ea60084360e5b434d1a2fd5cd4e09fc0a180b94/springfield/firefox/views.py#L438) view and will respond with one of a few templates. One of those templates is highly flexible and is frequently served at other URLs as well.

# By URL

## / (home)

When a user requests `/` the [DownloadView](https://github.com/mozmeao/springfield/blob/5ea60084360e5b434d1a2fd5cd4e09fc0a180b94/springfield/firefox/views.py#L438) view considers the following:

- country
- language (and that language's translation status)
- active switches
- URL parameters `v` (variation), `xv` (experience), and `reason` (`outdated`|`manual_update`).

It then responds with the first template that matches:

- `firefox/download/home.ftl` file is active and `xv` is not basic or legacy
    - *firefox/new/desktop/firefox-new-refresh.html*
- `firefox/download/desktop` file is active and `xv` is not basic
    - *firefox/new/desktop/download.html*
- no ftl files are active or `xv` is basic
    - *firefox/new/basic/base_download.html*

These templates all use the basic `download_firefox_thanks` helper and serve release Firefox in the language of the current page for the platform (aka operating system) that bedrock has auto-detected.

## /windows, /mac, /linux (the platform pages)

The "platform" pages [windows](https://www.firefox.com/browsers/desktop/windows/), [mac](https://www.firefox.com/browsers/desktop/mac), [linux](https://www.firefox.com/browsers/desktop/linux/) are based on the templates in *firefox/download/basic/*.

These pages use the more complicated `download_firefox` download helper to link directly to the specified platform.

## /channel (the channel pages)

[channel pages](https://www.firefox.com/channel/desktop/)

## /all

Firefox is available in more languages than the website is. The /all pages were originally implemented as a way for a user to download a copy of Firefox in a language that the website does not support. It has since ballooned as a way to get a highly configured version of Firefox.

This app is in desperate need of a UX re-think. The templates it uses are in */templates/firefox/all/*

An older copy of /all is also served as a [fall back page for the entire site](https://github.com/mozmeao/www-error-page) in some conditions.


# By Template

## templates/firefox/download/basic/*

Originally created in 2018, this simple template has been preserved because of its wide translation status. See it in English by appending `?xv=legacy` to the URL. This download page was the first to focus specifically on the desktop version of Firefox, prior to this all platforms were advertised on the download page.

It's also used to create the high converting platform pages which target searches for "Download Firefox for { platform }".

## templates/firefox/download/desktop/base.html

The base template extends the *base-protocol.html* template with some meta data specific to Firefox downloads.

The base template frequently gets used for variations and experiments including: [gaming](http://localhost:8000/en-GB/firefox/landing/gaming/) and [education](http://localhost:8000/en-GB/firefox/landing/education/).

### templates/firefox/download/desktop/download.html

Created in 2020 after a long very through design and user testing process -- this template promotes Desktop Firefox's features, use cases, personalization, mission, and platform support. (iOS and Android visitors get a banner and the download button is hidden.)

The first block on the page, which promotes the latest features, is hard-coded so avoid putting preasure on the localization community to translate frequently updating marketing content. (It turns out this section doesn't change that often though...)

The CTAs are in content blocks and can be swapped out for variations and experiments for example: [tech](http://localhost:8000/en-GB/firefox/landing/tech/) and [get](http://localhost:8000/en-GB/firefox/landing/get/).

### templates/firefox/download/home.html

Created in 2025 to reflect the changing Firefox brand this template focuses on our updated messaging, voice, and tone.

## Experiments

Rather than adding an experiment directly to one of the existing templates we typically duplicate or extend the template and add it to the view.

For details on configuring an a/b test see [A/B testing](../abtest.md).


