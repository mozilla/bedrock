# Managing Data Privacy and Consent {: #consent_management }

Please see the internal [Confluence page](https://mozilla-hub.atlassian.net/wiki/spaces/EN/pages/538050566/Cookie+Banner+Implementation+On+Mozilla.org) on Mozilla's overall approach to handling data privacy and cookie consent management on www.mozilla.org. This page will include detailed legal guidance and FAQs on the permitted use of tracking technologies.

Here we will cover bedrock's technical approach to implementing data consent per that legal guidance, whilst also balancing UX considerations and input from other teams.

In [EU and EAA countries](https://www.gov.uk/eu-eea) where explicit consent to cookies and analytics is required, there are certain web page URLs where bedrock will display a cookie consent banner. These URLs are stored in a strict [allow-list](https://github.com/mozilla/bedrock/tree/main/media/js/base/consent/allow-list.es6.js). URLs that are not in this list will neither show a banner, nor load any non-necessary cookies / analytics in the EU/EAA. The intent here is to provide as little disruption for our website visitors as possible, whilst still allowing opt-in to analytics URLs such as campaign pages. It is also possible to force the banner to show on any EU page by adding a query parameter ``?mozcb=y`` (used for specific campaign traffic sources such as advertisements).

Visitors in the EU/EAA countries can also send an opt-out signal by enabling either [Global Privacy Control](https://developer.mozilla.org/docs/Web/API/Navigator/globalPrivacyControl) (GPC) and [Do Not Track](https://developer.mozilla.org/docs/Web/API/Navigator/doNotTrack) (DNT) in their browser. If either of these signals are enabled then we do not show a banner. Individual cookie preferences can also be updated via a dedicated [cookie settings page](https://www.mozilla.org/privacy/websites/cookie-settings/) linked in the main footer.

In non-EU/EAA countries, non-necessary cookies and analytics are loaded by default. Visitors can still opt out via the [cookie settings page](https://www.mozilla.org/privacy/websites/cookie-settings/). Enabling GPC / DNT will also act as an opt-out signal where needed.

There is a [Figma flowchart](https://www.figma.com/file/DRdAbRUqi2EYynCx13dTfB/www.mozilla.org-cookie---Cookie-Consent-Flowchart?type=whiteboard&node-id=0%3A1&t=GbhFf7ZCC5XcQR29-1) detailing the general flow of logic. The code that implements this logic can be found in the `media/js/base/consent` directory.

## Related dependencies

For more detail documentation on dependencies used for consent management, see their respective GitHub repositories.

-   [Cookie consent banner repo](https://github.com/mozmeao/consent-banner/)
-   [Cookie helper repo](https://github.com/mozmeao/cookie-helper/)
-   [DNT helper repo](https://github.com/mozmeao/dnt-helper/)

## Debugging consent state

Occasionally people will come along and say "I don't see the cookie banner, is something broken!?". The answer is typically that they do not meet the criteria in order to require seeing it. To help debug, you can ask them to paste the following line of code in their browser's web console:

```javascript
window.Mozilla.getConsentStateMsg()
```

This will output one of the following state message strings:

- `STATE_GPC_ENABLED` - Their browser has GPC enabled.
- `STATE_DNT_ENABLED` - Their browser has DNT enabled.
- `STATE_HAS_CONSENT_COOKIE` - They already have a consent cookie that either accepts or rejects non-essential cookies.
- `STATE_SHOW_COOKIE_BANNER` - Consent to non-essential cookies is required (the banner should be visible).
- `STATE_BANNER_NOT_PERMITTED` - The page URL is not in the explicit allow-list for the cookie banner to display.
- `STATE_COOKIES_PERMITTED` - Non-essential cookies are permitted without explicit consent (e.g. the visitor is located in the US).
