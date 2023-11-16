---
title: Pocket mode
---

# Google Tag Manager (GTM)

In pocket mode, bedrock also uses Google Tag Manager (GTM) to manage and
organize its Google Analytics (GA4) solution. This is mostly for
marketing's own use, and is not used by the Pocket organization.

In contrast to mozorg mode, GA in Pocket is mostly used for measuring a
few key events, such as sign ups and logged-in / logged-out page views.
Most of this event and triggering logic exists entirely inside GTM, as
opposed to in bedrock code.

# Snowplow

[Snowplow](https://snowplow.io/) is the analytics tool used by the
Pocket organization, which is something marketing has limited access to.
Snowplow is mostly used for tracking events in the Pocket web
application, although we do also load it on the logged-out marketing
pages that are hosted by bedrock.

# How can visitors opt out of Pocket analytics?

Pocket website visitors can opt-out of both GA and Snowplow by changing
their preferences in the [One Trust Cookie
Banner](https://www.onetrust.com/) we display on page load. If someone
opts-out of analytics cookies, we do not load GA, however we do still
load Snowplow in a more privacy reserved mode.

Snowplow configuration with cookie consent (default):

``` javascript
{
    appId: SNOWPLOW_APP_ID,
    platform: 'web',
    eventMethod: 'beacon',
    respectDoNotTrack: false,
    stateStorageStrategy: 'cookieAndLocalStorage',
    contexts: {
        webPage: true,
        performanceTiming: true
    },
    anonymousTracking: false
}
```

Snowplow configuration without cookie consent:

``` javascript
{
    appId: SNOWPLOW_APP_ID,
    platform: 'web',
    eventMethod: 'post',
    respectDoNotTrack: false,
    stateStorageStrategy: 'none',
    contexts: {
        webPage: true,
        performanceTiming: true
    },
    anonymousTracking: {
        withServerAnonymisation: true
    }
}
```

See our [Pocket analytics
code](https://github.com/mozilla/bedrock/blob/main/media/js/pocket/analytics.es6.js)
for more details.
