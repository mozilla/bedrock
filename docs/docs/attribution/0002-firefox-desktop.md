# Firefox desktop attribution {: #firefox_desktop_attribution }

Firefox Desktop Attribution (often referred to as Stub Attribution) is a system that enables Mozilla to link website attributable referral data (including Google Analytics data) to a user's Firefox profile. When a website visitor lands on www.mozilla.org and clicks to download Firefox, we pass attribution data about their visit to the Firefox installer for inclusion in [Telemetry](https://telemetry.mozilla.org/). This is to enable Mozilla to better understand how changes to our website and different marketing campaigns can affect installation rates, as well as overall product retention. The data also gives us an insight into how many installations originate from www.mozilla.org, as opposed to elsewhere on the internet.

## Scope and requirements

-   Attribution was originally only possible via the Firefox stub installer on Windows (hence the name *stub attribution*), however it now also works on full installer links, and across all desktop release channels.
-   Attribution now also works on macOS. The flow does not yet work for Linux, Android or iOS devices.
-   Attribution will only be passed if a website visitor has their [Do Not Track (DNT)](https://support.mozilla.org/kb/how-do-i-turn-do-not-track-feature) and [Global Privacy Control (GPC)](https://support.mozilla.org/kb/global-privacy-control) preferences disabled in their browser. Visitors can opt-out by enabling DNT or GPC. This is covered in our [privacy policy](https://www.mozilla.org/privacy/websites/).

## How does attribution work?

See the [Application Logic Flow Chart](https://www.figma.com/file/q5mJpicWBpzAYuQ3fV00ix/Firefox-Stub-Attribution-Flow?node-id=0%3A1&t=EFe91WQzQ7cXHSiB-1) for a more detailed visual representation of the steps below (Mozilla access only).

1.  A user visits a page on www.mozilla.org. On page load, a [JavaScript function](https://github.com/mozilla/bedrock/blob/main/media/js/base/stub-attribution.js) collects referral and analytics data about from where their visit originated (see the table below for a full list of attribution data we collect).
2.  Once the attribution data is validated, bedrock then generates an attribution session ID. This ID is included in the user's attribution data, and is also sent to Google Analytics as a non-interaction event.
3.  Next we send the attribution data to an authentication service that is part of bedrock's back-end server. The data is validated again, then base64 encoded and returned to the client together with an signed, encrypted signature to prove that the data came from www.mozilla.org.
4.  The encoded attribution data and signature are then stored as cookies in the user's web browser. The cookies have the IDs `moz-stub-attribution-code` (the attribution code) and `moz-stub-attribution-sig` (the encrypted signature). Both cookies have a 24 hour expiry.
5.  Once the user reaches a Firefox download page, bedrock then checks if both attribution cookies exist, and if so appends the authenticated data to the Firefox download link. The query parameters are labelled `attribution_code` and `attribution_sig`.
6.  When the user clicks the Firefox download link, another attribution service hosted at `download.mozilla.org` then decrypts and validates the attribution signature. If the secret matches, a unique download token is generated. The service then stores both the attribution data (including the Google Analytics client ID) and the download token in Mozilla's private server logs.
7.  The service then passes the download token and attribution data (excluding the GA client ID) into the installer being served to the user.
8.  Once the user installs Firefox, the data that was passed to the installer is then stored in the users' Telemetry profile.
9.  During analysis, the download token can be used to join Telemetry data with the corresponding GA data in the server logs.

!!! note
    The stub attribution script uses the attribute `data-download-version` to identify what links are download links.


## Attribution data

| Name            | Description                                                                             | Example                  |
| --------------- | --------------------------------------------------------------------------------------- | ------------------------ |
| `utm_source`    | Query param identifying the referring site which sent the visitor.                      | `utm_source=google`      |
| `utm_medium`    | Query param identifying the type of link, such as referral, cost per click, or email.   | `utm_medium=cpc`         |
| `utm_campaign`  | Query param identifying the specific marketing campaign that was seen.                  | `utm_campaign=fast`      |
| `utm_content`   | Query param identifying the specific element that was clicked.                          | `utm_content=getfirefox` |
| `referrer`      | The domain of the referring site when the link was clicked.                             | `google.com`             |
| `ua`            | Simplified browser name parsed from the visitor's User Agent string.                   | `chrome`                 |
| `experiment`    | Query param identifying an experiment name that visitor was a cohort of.                | `taskbar`                |
| `variation`     | Query param identifying the experiment variation that was seen by the visitor.          |                          |
| `client_id_ga4` | Google Analytics 4 Client ID.                                                           | `1715265578.1681917481`  |
| `session_id`    | A random 10 digit string identifier used to associate attribution data with GA session. | `9770365798`             |
| `dlsource`      | A hard-coded string ID used to distinguish mozorg downloads from archive downloads      | `mozorg`                 |

!!! note
    If any of the above values are not present then a default value of `(not set)` will be used.


## Cookies

The cookies created during the attribution flow are as follows:

| Name                        | Value                             | Domain            | Path | Expiry   |
| --------------------------- | --------------------------------- | ----------------- | ---- | -------- |
| `moz-stub-attribution-code` | Base64 encoded attribution string | `www.mozilla.org` | `/`  | 24 hours |
| `moz-stub-attribution-sig`  | Base64 encoded signature          | `www.mozilla.org` | `/`  | 24 hours |

## Measuring campaigns and experiments

Firefox Desktop Attribution was originally designed for measuring the effectiveness of marketing campaigns where the top of the funnel was outside the remit of www.mozilla.org. For these types of campaigns, stub attribution requires zero configuration. It just works in the background and passes along any attribution data that exists.

It is also possible to measure the effectiveness of experiments on installation rates and retention. This is achieved by adding optional `experiment` and `variation` parameters to a page URL. Additionally, these values can also be set via JavaScript using:

``` javascript
Mozilla.StubAttribution.experimentName = 'experiment-name';
Mozilla.StubAttribution.experimentVariation = 'v1';
```

!!! note
    When setting a experiment parameters using JavaScript like in the example above, it must be done prior to calling `Mozilla.StubAttribution.init()`.


## Download as Default

[Download as default](../firefox-downloads/desktop-download-as-default.md) is a feature that communicates to the
stub installer that the browser should be set as default when downloaded. At the moment this feature is hijacking
the stub attribution service to communicate this and it will over-write other attribution data.

## Return to addons.mozilla.org (RTAMO)

[Return to AMO](https://wiki.mozilla.org/Add-ons/QA/Testplan/Return_to_AMO) (RTAMO) is a Firefox feature whereby a first-time installation onboarding flow is initiated, that redirects a user to install the extension they have chosen whilst browsing [AMO](https://addons.mozilla.org/firefox/) using a different browser. RTAMO works by leveraging the existing stub attribution flow, and checking for specific `utm_` parameters that were passed if the referrer is from AMO.

Specifically, the RTAMO feature looks for a `utm_content` parameter that starts with `rta:`, followed by an ID specific to an extension. For example: `utm_content=rta:dUJsb2NrMEByYXltb25kaGlsbC5uZXQ`. The stub attribution code in bedrock also checks the referrer before passing this on, to make sure the links originate from AMO. If RTAMO data comes from a domain other than AMO, then the attribution data is dropped.

RTAMO initially worked for only a limited subset of addons recommended by Mozilla. This functionality was recently expanded by the AMO team to cover all publically listed addons, under a project called ``Extended RTAMO (ERTAMO)``.

!!! important
    Because RTAMO is a user facing feature, expressly requested by the user from the AMO page, we deem the RTAMO flow as an essential/necessary use of attribution data. We do however limit the amount of data we collect to only what's essential for the RTAMO to function as a feature. Non-essential fields such as the Google Analytics client ID are omitted. We also continue to respect Do Not Track (DNT) as a valid opt-out signal.


## How can visitors opt out?

Visitors to the website can opt-out of desktop attribution on our website by enabling [Do Not Track (DNT)](https://support.mozilla.org/kb/how-do-i-turn-do-not-track-feature) in their web browser. We facilitate this by using a [DNT helper](https://github.com/mozmeao/dnt-helper) that our team maintains.

## Local testing

For stub attribution to work locally or on a demo instance, a value for the HMAC key that is used to sign the attribution code must be set via an environment variable e.g.

``` html
STUB_ATTRIBUTION_HMAC_KEY=thedude
```

!!! note
    This value can be anything if all you need to do is test the bedrock functionality. It only needs to match the value used to verify data passed to the stub installer for full end-to-end testing via Telemetry.


## Manual testing for code reviews

You might not need to test all these depending on what is changing this is an exhaustive testing guide. This guide assumes demo1, make sure you're testing on the right URL.

1.  Use Chrome on Windows or MacOS with DNT and adblocking disabled.

2.  Open <https://www-demo1.allizom.org/en-US/?utm_source=ham&utm_campaign=pineapple>

3.  Using Dev Tools, open the Application tab and inspect cookies.

4.  Look for a cookie called ``moz-stub-attribution-code`` and copy the value (it should be a base64 encoded string).

5. Decode the base64 string (e.g. using <https://base64decode.org>) and check that:

    -   ``dlsource`` parameter value is mozorg
    -   ``client_id_ga4`` and ``session_id`` parameters exist
    -   ``client_id_ga4`` should look something like 0700077325.1656063224 (the numbers will differ but the format with the middle period should look the same).
    -   ``source`` and ``campaign`` have the values ham and pineapple, respectively.
    -   The ua value should be chrome (assuming you tested in Chrome).
    -   Everything else should be (not set).

6.  Inspect the "Download Firefox" button in the top right and verify the download URL contains ``attribution_code`` and ``attribution_sig`` params.

7.  Click "Download Firefox".

8.  Inspect the "Try downloading again" link and check for the ``attribution_code`` and ``attribution_sig`` params.
    -   decode the value of ``attribution_code`` to check it has the expected values

Other places on the site you may want to check:

-   [firefox/all](https://www-demo1.allizom.org/en-US/firefox/all/) (inspect the network request to check that the attribution params were added on click)
-   [firefox/new](https://www-demo1.allizom.org/en-US/firefox/new/)
-   [firefox/enterprise](https://www-demo1.allizom.org/en-US/firefox/enterprise/)
