# Banners

## Creating page banners

Any page on bedrock can incorporate a top of page banner as a temporary feature. An example of such a banner is the `MOFO (Mozilla Foundation)`{.interpreted-text role="abbr"} fundraising banner that gets shown on the home page several times a year.

Banners can be inserted into any page template by using the `page_banner` block. Banners can also be toggled on and off using a switch:

``` jinja
{% block page_banner %}
  {% if switch('fundraising-banner') %}
    {% include 'includes/banners/fundraiser.html' %}
  {% endif %}
{% endblock %}
```

Banner templates should extend the *basic banner template*, which provides very unopinionated structure but includes several helpful features such as a close button with localized text and exclusion of banner content from search result snippets.

Custom banner content can then be inserted using `banner_title` and `banner_content` blocks:

``` jinja
{% extends 'includes/banners/basic.html' %}

{% block banner_title %}We all love the web. Join Mozilla in defending it.{% endblock %}

{% block banner_content %}
    <!-- insert custom HTML here -->
{% endblock %}
```

To initiate a banner on a page, include `js/base/banners/mozilla-banner.js` in your page bundle and then initiate the banner using a unique ID. The ID will be used as a cookie identifier should someone dismiss a banner and not wish to see it again.

``` javascript
(function() {
    'use strict';

    function onLoad() {
        window.Mozilla.Banner.init('fundraising-banner');
    }

    window.Mozilla.run(onLoad);

})();
```

By default, page banners will be rendered directly underneath the primary page navigation. If you want to render a banner flush at the top of the page, you can pass a secondary `renderAtTopOfPage` parameter to the `init()` function with a boolean value:

``` javascript
(function() {
    'use strict';

    function onLoad() {
        window.Mozilla.Banner.init('fundraising-banner', true);
    }

    window.Mozilla.run(onLoad);

})();
```

### L10n for page banners

Because banners can technically be shown on any page, they need to be broadly translated, or alternatively limited to the subset of locales that have translations. Each banner should have its own `.ftl` associated with it, and accessible to the template or view it gets used in.
