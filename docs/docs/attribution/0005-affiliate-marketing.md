# Mozilla CJMS affiliate attribution {: #affiliate_attribution }

The CJMS affiliate attribution flow comprises an integration between the [Commission Junction (CJ)](https://www.cj.com/) affiliate marketing event system, bedrock, and the Security and Privacy team's [CJ micro service (CJMS)](https://github.com/mozilla-services/cjms).

The system allows individuals who partner with Mozilla, via CJ, to share referral links for Mozilla with their audiences. When people subscribe using an affiliate link, the partner can be attributed appropriately in CJ's system.

## How does attribution work?

For a more detailed breakdown you can view the [full flow diagram](https://www.figma.com/file/6jnLCLzclBN0uyS4nJp57d/Affiliate-Marketing-(CJ)-Architecture-%2F-Flow) (Mozilla access only), but at a high level the logic that bedrock is responsible for is as follows:

1.  On pages which include the script, on page load, a [JavaScript function](https://github.com/mozilla/bedrock/blob/main/media/js/products/vpn/affiliate-attribution.es6.js) looks for a `cjevent` query parameterin the page URL.
2.  If found, we validate the query param value and then `POST` it together with a Firefox Account `flow_id` to the CJMS.
3.  The CJMS responds with an affiliate marketing ID and expiry time, which we then set as a first-party cookie. This cookie is used to maintain a relationship between the `cjevent` value and an individual `flow_id`, so that successful subscriptions can be properly attributed to CJ.
4.  If a website visitor later returns to the page with an affiliate marketing cookie already set, then we update the `flow_id` and `cjevent` value (if a new one exists) via `PUT` on their repeat visit. This ensures that the most recent CJ referral is attributed if/when someone decides to purchase a subscription.
5.  The CJMS then responds with an updated ID / expiry time for the affiliate marketing cookie.

## How can visitors opt out?

1.  To facilitate an opt-out of attribution, we display a cookie notification with an opt-out button at the top of the page when the flow initiates.
2.  If someone clicks "Reject" to opt-out, we generate a new `flow_id` (invalidating the existing `flow_id` in the CJMS database) and then delete the affiliate marketing cookie, replacing it with a "reject" preference cookie that will prevent attribution from initiating on repeat visits. This preference cookie will expire after 1 month.
3.  If someone clicks "OK" or closes the opt-out notification by clicking the "X" icon, here we assume the website visitor is OK with attribution. We set an "accept" preference cookie that will prevent displaying the opt-out notification on future visits (again with a 1 month expiry) and allow attribution to flow.

## Cookies

The affiliate cookie has the following configuration:

| Cookie name          | Value        | Domain              | Expiry  |
| -------------------- | ------------ | ------------------- | ------- |
| `moz-cj-affiliate`   | Affiliate ID | `www.mozilla.org`   | 30 days |

!!! note
    To query what version of CJMS is currently deployed at the endpoint bedrock points to, you can add `__version__` at the end of the base URL to see the release number and commit hash. For example: <https://stage.cjms.nonprod.cloudops.mozgcp.net/__version__>
