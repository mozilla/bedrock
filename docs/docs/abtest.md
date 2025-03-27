---
render_macros: true
---

# A/B Testing {: #ab_testing }

## Traffic Cop experiments

More complex experiments, such as those that feature full page redesigns, or multi-page user flows, should be implemented using [Traffic Cop](https://github.com/mozmeao/trafficcop/). Traffic Cop small javascript library which will direct site traffic to different variants in a/b experiments and make sure a visitor always sees the same variation.

It's possible to test more than 2 variants.

Traffic Cop sends users to experiments and then we use Google Analytics (GA) to analyze which variation is more successful. (If the user has `DNT (Do Not Track)`{.interpreted-text role="abbr"} or `GPC (Global Privacy Control)`{.interpreted-text role="abbr"} enabled they do not participate in experiments.)

All a/b tests should have a [mana page](https://mana.mozilla.org/wiki/display/EN/Details+of+experiments+by+mozilla.org+team) detailing the experiment and recording the results.

### Coding the variants

Traffic cop supports two methods of a/b testing. Executing different on page javascript or redirecting to the same URL with a query string appended. We mostly use the redirect method in bedrock. This makes testing easier.

Create a [variation view](coding.md#variation-views) for the a/b test.

The view can handle the URL redirect in one of two ways:

1.  the same page, with some different content based on the ``variation`` variable
2.  a totally different page

### Content variation

Useful for small focused tests.

This is explained on the [variation view](coding.md#variation-views) page.

### New page

Useful for large page changes where content and assets are dramatically different.

Create the variant page like you would a new page. Make sure it is `noindex` and does not have a `canonical` URL.

``` jinja
{% block canonical_urls %}<meta name="robots" content="noindex,follow">{% endblock %}
```

Configure as explained on the [variation view](coding.md#variation-views) page.

### Traffic Cop

Create a .js file where you initialize Traffic Cop and include that in the experiments block in the template that will be doing the redirection. Wrap the extra js include in a [switch](install.md#feature-flipping-aka-switches-or-waffle-switches).

``` jinja
{% block experiments %}
  {% if switch('experiment-berlin-video', ['de']) %}
    {{ js_bundle('firefox_new_berlin_experiment') }}
  {% endif %}
{% endblock %}
```

### Switches

See the traffic cop section of the [switch docs](install.md#feature-flipping-aka-switches-or-waffle-switches) for instructions.

### Recording the data

!!! note
    If you are measuring installs as part of your experiment be sure to configure [custom stub attribution](attribution/0002-firefox-desktop.md#measuring-campaigns-and-experiments) as well.


Send the experiment view events to GA4 with the event name `experiment_view`. The `id` of all variants should be the same and all `variant` values should be unique.

Make sure any buttons and interaction which are being compared as part of the test will report into `GA (Google Analytics)`{.interpreted-text role="abbr"}.

``` javascript
if (href.indexOf('v=a') !== -1) {
    // GA4
    window.dataLayer.push({
        event: 'experiment_view',
        id: 'Berlin-Campaign-Landing-Page',
        variant: 'de-page',
    });
} else if (href.indexOf('v=b') !== -1) {
    // GA4
    window.dataLayer.push({
        event: 'experiment_view',
        id: 'Berlin-Campaign-Landing-Page',
        variant: 'campaign-page',
    });
}
```

### Viewing the data

We have not figured this out for GA4 yet.

### Tests

Write some tests for your a/b test. This could be simple or complex depending on the experiment.

Some things to consider checking:

-   Requests for the default (non variant) page call the correct template.
-   Requests for a variant page call the correct template.
-   Locales excluded from the test call the correct (default) template.

## Avoiding experiment collisions

To ensure that Traffic Cop doesn't overwrite data from any other externally controlled experiments (for example Ad campaign tests, or in-product Firefox experiments), you can use the experiment-utils helper to decide whether or not Traffic Cop should initiate.

``` javascript
import TrafficCop = from '@mozmeao/trafficcop';
import { isApprovedToRun } from '../../base/experiment-utils.es6';

if (isApprovedToRun()) {
    const cop = new TrafficCop({
        variations: {
            'entrypoint_experiment=experiment-name&entrypoint_variation=a': 10,
            'entrypoint_experiment=experiment-name&entrypoint_variation=b': 10
        }
    });

    cop.init();
}
```

The `isApprovedToRun()` function will check the page URL's query parameters against a list of well-known experimental params, and return `false` if any of those params are found. It will also check for some other cases where we do not want to run experiments, such as if the page is being opened in an automated testing environment.
