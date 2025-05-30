---
render_macros: true
---

# Mozilla VPN Subscriptions {: #vpn_subscriptions }

The [Mozilla VPN landing page](https://www.mozilla.org/en-US/products/vpn/) displays both pricing and currency information that is dependant on someone's physical location in the world (using geo-location). If someone is in the United States, they should see pricing in \$USD, and if someone is in Germany they should see pricing in Euros. The page is also available in multiple languages, which can be viewed independently of someone's physical location. So someone who lives in Switzerland, but is viewing the page in German, should still see pricing and currency displayed in Swiss Francs (CHF).

Additionally, it is important that we render location specific subscription links, as purchasing requires a credit card that is registered to each country where we have a plan available. We are also legally obligated to prevent both purchasing and/or downloading of Mozilla VPN in certain countries. In countries where VPN is not yet available, we also rely on geo-location to hide subscription links, and instead to display a *call to action* to encourage prospective customers to sign up to the [VPN wait list](https://www.mozilla.org/en-US/products/vpn/invite/).

To facilitate all of the above, we rely on our CDN to return an appropriate country code that relates to where a visitor's request originated from (see [Geo Template View](coding.md#geo-location)). We use that country code in our helpers and view logic for the VPN landing page to decide what to display in the pricing section of the page (see ``Mozilla :abbr:`VPN (Virtual Private Network)`` Links <mozilla-accounts.rst#vpn-helpers>`_).

## Server architecture

Bedrock is configured so that when `dev=True`, VPN subscription links will point to the Mozilla accounts staging environment. When `dev=False`, they will point to the Fxa production environment.

So our different environments are mapped like so:

-   `http://localhost:8000` -> `https://accounts.stage.mozaws.net/`
-   `https://www-dev.allizom.org/products/vpn/` -> `https://accounts.stage.mozaws.net/`
-   `https://www.allizom.or/products/vpn/` -> `https://accounts.firefox.com/`
-   `https://www.mozilla.org/products/vpn` -> `https://accounts.firefox.com/`

This allows the product and QA teams to routinely test changes and new VPN client releases on <https://www-dev.allizom.org/products/vpn/>, prior to being available in production.

## Adding new countries for VPN

When launching VPN in new countries there is a set process to follow.

### Launch steps

1.  All the code changes below should be added **behind a feature switch**.
2.  Once the PR is reviewed and merged, the product QA team should be notified and they can then perform testing on <https://www-dev.allizom.org/products/vpn/>. Often the QA team will request a date for code to be ready for testing to begin.
3.  Code can be pushed to production ahead of time (but will be disabled behind the feature switch by default).
4.  Once QA gives the green light on launch day, the feature switch can then be enabled in production.
5.  QA will then do a final round of post-launch QA to verify subscriptions / purchasing works in the new countries in production.

### Code changes

Reference: officially assigned list of [ISO country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements). Reference: list of [ISO 4217 currency codes](https://en.wikipedia.org/wiki/ISO_4217#Active_codes)`

The majority of config changes need to happen in `bedrock/settings/base.py`:

1.  Add new pricing plan configs to `VPN_PLAN_ID_MATRIX` for any new countries that require newly created plan IDs (these will be provided by the VPN team). Separate plan IDs for both dev and prod are required for each new currency / language combination (this is because the product QA team need differently configured plans on dev to routinely test things like renewal and cancellation flows). Meta data such as price, total price and saving for each plan / currency should also be provided.

    Example pricing plan config for \$USD / English containing both 12-month and monthly plans:

    > ``` python
    > ```
    >
    > VPN_PLAN_ID_MATRIX = {
    >
    > :
    >
    >     "usd": {
    >
    >     :
    >
    >         "en": {
    >
    >         :
    >
    >             "12-month": {
    >
    >             :
    >
    >                 "id": (
    >
    >                 :   "price_1J0Y1iKb9q6OnNsLXwdOFgDr" if DEV else "price_1Iw85dJNcmPzuWtRyhMDdtM7"
    >
    >                 ), "price": "US\$4.99", "total": "US\$59.88", "saving": 50, "analytics": { "brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "60.00", "price": "59.88", "period": "yearly", },
    >
    >             }, "monthly": { "id": ( "price_1J0owvKb9q6OnNsLExNhEDXm" if DEV else "price_1Iw7qSJNcmPzuWtRMUZpOwLm" ), "price": "US\$9.99", "total": None, "saving": None, "analytics": { "brand": "vpn", "plan": "vpn", "currency": "USD", "discount": "0", "price": "9.99", "period": "monthly", }, },
    >
    >         }
    >
    >     }, \# repeat for other currency / language configs.
    >
    > }
    >
    > See the *Begin Checkout* section of the `analytics docs<analytics>`{.interpreted-text role="ref"} for more a detailed description of what should be in the analytics objects.

2.  Map each new country code to one or more applicable pricing plans in `VPN_VARIABLE_PRICING`.

    Example that maps the `US` country code to the pricing plan config above:

    > ``` python
    > ```
    >
    > VPN_VARIABLE_PRICING = {
    >
    > :
    >
    >     "US": {
    >
    >     :   "default": VPN_PLAN_ID_MATRIX["usd"]["en"],
    >
    >     }, \# repeat for other country codes.
    >
    > }

3.  Once every new country has a mapping to a pricing plan, add each new country code to the list of supported countries in `VPN_COUNTRY_CODES`. Because new countries need to be added behind a feature switch, you may want to create a new variable temporarily for this until launched, such as `VPN_COUNTRY_CODES_WAVE_VI`. You can then add these to `VPN_COUNTRY_CODES` in `products/views.py` using a simple function like so:

    > ``` python
    > ```
    >
    > def vpn_available(request):
    >
    > :   country = get_country_from_request(request) country_list = settings.VPN_COUNTRY_CODES
    >
    >     if switch("vpn-wave-vi"):
    >
    >     :   country_list = settings.VPN_COUNTRY_CODES + settings.VPN_COUNTRY_CODES_WAVE_VI
    >
    >     return country in country_list
    >
    > The function could then be used in the landing page view like so:
    >
    > ``` python
    > ```
    >
    > vpn_available_in_country = (vpn_available(request),)

4.  If you now test the landing page locally, you should hopefully see the newly added pricing for each new country (add the `?geo=[INSERT_COUNTRY_CODE]` param to the page URL to mock each country). If all is well, this is the perfect time to add new [unit tests](https://github.com/mozilla/bedrock/blob/main/bedrock/products/tests/test_helper_misc.py) for each new country. This will help give you confidence that the right plan ID is displayed for each new country / language option.

    ``` python
    def test_vpn_subscribe_link_variable_12_month_us_en(self):
        """Should contain expected 12-month plan ID (US / en-US)"""
        markup = self._render(
            plan="12-month",
            country_code="US",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Iw85dJNcmPzuWtRyhMDdtM7", markup)


    def test_vpn_subscribe_link_variable_monthly_us_en(self):
        """Should contain expected monthly plan ID (US / en-US)"""
        markup = self._render(
            plan="monthly",
            country_code="US",
            lang="en-US",
        )
        self.assertIn("?plan=price_1Iw7qSJNcmPzuWtRMUZpOwLm", markup)
    ```

5.  Finally, update `VPN_AVAILABLE_COUNTRIES` to the new total number of countries where VPN is available. Again, because this needs to be behind a feature switch you may want a new temporary variable that you can use in `products/views.py`:

    ``` python
    available_countries = settings.VPN_AVAILABLE_COUNTRIES

    if switch("vpn-wave-vi"):
        available_countries = settings.VPN_AVAILABLE_COUNTRIES_WAVE_VI
    ```

6.  After things are launched in production and QA has verified that all is well, don't forget to file an issue to tidy up the temporary variables and switch logic.

## Excluded countries

For a list of country codes where we are legally obligated to prevent purchasing VPN, see `VPN_EXCLUDED_COUNTRY_CODES` in `bedrock/settings/base.py`.

For a list of country codes where we are also required to prevent downloading the VPN client, see `VPN_BLOCK_DOWNLOAD_COUNTRY_CODES`.
