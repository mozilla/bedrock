---
title: Browser Support
---

We seek to provide usable experiences of our most important web content
to all user agents. But newer browsers are far more capable than older
browsers, and the capabilities they provide are valuable to developers
and site visitors. We **will** take advantage of modern browser
capabilities. Older browsers **will** have a different experience of the
website than newer browsers. We will strike this balance by generally
adhering to the core principles of [Progressive
Enhancement](https://en.wikipedia.org/wiki/Progressive_enhancement):

> -   Basic content should be accessible to all web browsers
> -   Basic functionality should be accessible to all web browsers
> -   Sparse, semantic markup contains all content
> -   Enhanced layout is provided by externally linked CSS
> -   Enhanced behavior is provided by unobtrusive, externally linked
>     JavaScript
> -   End-user web browser preferences are respected

Some website experiences may require us to deviate from these principles
\-- imagine *a marketing campaign page built under timeline pressure to
deliver novel functionality to a particular locale for a short while*
\-- but those will be exceptions and rare.

# Browser Support Matrix

*Last updated: Updated July 19, 2023*

## Firefox

It is important for website visitors to be able to download Firefox on a
very broad range of desktop operating systems. As such, we aim to
deliver enhanced support to user agents in our browser support matrix
below.

**Enhanced support:**

> Windows 11 and above
>
> :   -   All evergreen browsers
>         -   Firefox
>         -   Firefox ESR
>         -   Chrome
>         -   Edge
>         -   Brave
>         -   Opera
>
> Windows 10
>
> :   -   All evergreen browsers
>
> macOS 10.15 and above
>
> :   -   All evergreen browsers
>     -   Safari
>
> Linux
>
> :   -   All evergreen browsers

**Degraded support:**

Website visitors on slightly older browsers fall under degraded support,
which means that the website should be fully readable and accessible,
but they may not get enhanced CSS layout or JS features.

> Windows 10
>
> :   -   Internet Explorer 11
>
> Windows 8.1 and below
>
> :   -   Firefox 115
>     -   Chrome 109
>     -   Internet Explorer 10
>
> macOS 10.14 and below
>
> :   -   Firefox 115
>     -   Chrome 114
>     -   Safari 12.1

!!! note

    As of Firefox 116 (released August 1st 2023), support for Firefox has
    been ended on Windows 8.1 and below, as well as on macOS 10.14 and
    below. Website visitors on these outdated operating systems now fall
    under degraded support, and we offer them to download Firefox ESR
    instead.

**Basic support:**

Website visitors on very old versions of Internet Explorer will get only
a very basic universal CSS style sheet, and a basic no-JS experience.

> Windows 7
>
> :   -   Internet Explorer 9
>     -   Internet Explorer 8

**Unsupported:**

Even older versions of Internet Explorer are now unsupported.

> Windows XP / Vista
>
> :   -   Internet Explorer 7
>     -   Internet Explorer 6

!!! note

    Firefox ended support for Windows XP and Vista in 2017 with Firefox 53.
    Since then, we have continued to serve those users Firefox ESR 52
    instead. However, since then support for downloading has been
    discontinued. The SSL certificates on download.mozilla.org no longer
    support TLS 1.0.

## Privacy & security products

Browser support for our privacy and security products (such as VPN,
Relay, Monitor etc) is thankfully a simpler story. Since all these
product use a Firefox account for authentication, we can simply follow
the [Firefox Ecosystem
Platform](https://mozilla.github.io/ecosystem-platform/reference/browser-support)
browser support documentation.

The most notable thing here for bedrock is that Internet Explorer 11
does not need to be supported.

# Delivering basic support

On IE browsers that support [conditional
comments](https://wikipedia.org/wiki/Conditional_comment) (IE9 and
below), basic support consists of no page-specific CSS or JS. Instead,
we deliver well formed semantic HTML, and a universal CSS stylesheet
that gets applied to all pages. We do not serve these older browsers any
JS, with the exception of the following scripts:

- Google Analytics / GTM snippet.
- HTML5shiv for parsing modern HTML semantic elements.
- Stub Attribution script (IE8 / IE9).

Conditional comments should instead be used to handle content specific
to IE. To hide non-relevant content from IE users who see the universal
stylesheet, a `hide-from-legacy-ie` class name can also be applied
directly to HTML:

``` html
<p class="hide-from-legacy-ie">See what Firefox has blocked for you</p>
```

# Delivering degraded support

On other legacy browsers where conditional comments are not supported,
developers should instead rely on [feature
detection](https://developer.mozilla.org/docs/Learn/Tools_and_testing/Cross_browser_testing/Feature_detection)
to deliver a degraded experience where appropriate.

!!! note

    The following feature detection helpers will return true for all
    browsers that get enhanced support, but will also return true for IE11
    currently, even though that has now moved to degraded support. The
    reason for this is that whilst many of our newer products don't support
    IE at all (e.g. Mozilla VPN, Mozilla Monitor, Firefox Relay), we do
    still need to provide support so that IE users can easily download
    Firefox. We can decide to update the feature detect in the future, at a
    time when we think makes sense.

## Feature detection using CSS

For CSS, enhanced experiences can be delivered using [feature
queries](https://developer.mozilla.org/docs/Web/CSS/@supports), whilst
allowing older browsers to degrade gracefully using simpler layouts when
needed.

Additionally, there is also a universal CSS class hook available that
gets delivered via a site-wide JS feature detection snippet:

``` css
.is-modern-browser {
    /* Styles will only be applied to browsers that get enhanced support. */
}
```

## Feature detection using JavaScript

For JS, enhanced support can be delivered using a helper that leverages
the same feature detection snippet:

``` javascript
(function() {
    'use strict';

    function onLoad() {
        // Code that will only be run on browsers that get enhanced support.
    }

    window.Mozilla.run(onLoad);
})();
```

The `site.isModernBrowser` global property can also be used within
conditionals like so:

``` javascript
if (window.site.isModernBrowser) {
    // Code that will only be run on browsers that get enhanced support.
}
```

# Exceptions (Updated 2019-06-11)

Some pages of the website provide critical functionality to older
browsers. In particular, the Firefox desktop download funnel enables
users on older browsers to get a modern browser. To the extent possible,
we try to deliver enhanced experiences to all user agents on these
pages.

**The following pages get enhanced experiences for a longer list of user
agents:**

> -   `/firefox/`
> -   `/firefox/new/`
> -   `/firefox/download/thanks/`

!!! note

    An enhanced experience can be defined as a step above basic support.
    This can be achieved by delivering extra page-specific CSS to legacy
    browsers, or allowing them to degrade gracefully. It does not mean
    everything needs to [look the same in every
    browser](http://dowebsitesneedtolookexactlythesameineverybrowser.com/).

*[GTM]: Google Tag Manager
