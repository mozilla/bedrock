# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from decimal import Decimal

from django.conf import settings

import jinja2
from babel.core import UnknownLocaleError
from babel.numbers import format_currency
from django_jinja import library
from markupsafe import Markup

from bedrock.base.urlresolvers import reverse
from lib.l10n_utils.fluent import ftl

FTL_FILES = ["products/vpn/shared"]

# VPN ==================================================================


VPN_12_MONTH_PLAN = "12-month"

# Show price "+ tax" in countries such as US & Canada.
TAX_NOT_INCLUDED = ["US", "CA"]


def _format_currency(price, currency, currency_locale):
    # default to en_US if format_currency does not recognize the locale.
    try:
        amount = format_currency(price, currency, locale=currency_locale)
    except UnknownLocaleError:
        amount = format_currency(price, currency, locale="en_US")

    return amount


def _vpn_get_ga_data(selected_plan):
    id = selected_plan.get("id")
    analytics = selected_plan.get("analytics")

    ga_data = (
        "{"
        "'id' : '%s',"
        "'brand' : '%s',"
        "'plan' : '%s',"
        "'period' : '%s',"
        "'price' : '%s',"
        "'discount' : '%s',"
        "'currency' : '%s'"
        "}"
        % (
            id,
            analytics.get("brand"),
            analytics.get("plan"),
            analytics.get("period"),
            analytics.get("price"),
            analytics.get("discount"),
            analytics.get("currency"),
        )
    )

    return ga_data


def _vpn_get_available_plans(country_code, lang, bundle_relay=False):
    """
    Get subscription plan IDs using country_code and page language.
    Defaults to "US" if no matching country code is found.
    Each country also has a default language if no match is found.
    """

    if bundle_relay:
        country_plans = settings.VPN_RELAY_BUNDLE_PRICING.get(country_code, settings.VPN_RELAY_BUNDLE_PRICING["US"])
    else:
        country_plans = settings.VPN_VARIABLE_PRICING.get(country_code, settings.VPN_VARIABLE_PRICING["US"])

    return country_plans.get(lang, country_plans.get("default"))


def _vpn_product_link(product_url, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
    separator = "&" if "?" in product_url else "?"
    client_id = settings.VPN_CLIENT_ID
    href = f"{product_url}{separator}entrypoint={entrypoint}&form_type=button&service={client_id}&utm_source={entrypoint}&utm_medium=referral"

    if optional_parameters:
        params = "&".join(f"{param}={val}" for param, val in optional_parameters.items())
        href += f"&{params}"

    css_class = "js-fxa-product-cta-link js-fxa-product-button"
    attrs = ""

    if optional_attributes:
        attrs += " ".join(f'{attr}="{val}"' for attr, val in optional_attributes.items())

        # If there's a `data-cta-position` attribute for GA, also pass that as a query param to vpn.m.o.
        position = optional_attributes.get("data-cta-position", None)

        if position:
            href += f"&data_cta_position={position}"

    if class_name:
        css_class += f" {class_name}"

    markup = f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>' f"{link_text}" f"</a>"

    return Markup(markup)


@library.global_function
def vpn_available_in_country(country_code):
    """
    Global helper that can be passed a country_code via a template
    in order to determine if VPN is available in that country.
    """
    country_list = settings.VPN_COUNTRY_CODES
    return country_code in country_list


@library.global_function
@jinja2.pass_context
def vpn_subscribe_link(
    ctx,
    entrypoint,
    link_text,
    plan=VPN_12_MONTH_PLAN,
    class_name=None,
    country_code=None,
    lang=None,
    bundle_relay=False,
    optional_parameters=None,
    optional_attributes=None,
):
    """
    Render a vpn.mozilla.org subscribe link with required params for FxA authentication.

    Examples
    ========

    In Template
    -----------

        {{ vpn_subscribe_link(entrypoint='www.mozilla.org-vpn-product-page',
                              link_text='Get Mozilla VPN',
                              country_code=country_code,
                              lang=LANG) }}
    """

    if bundle_relay:
        product_id = settings.VPN_RELAY_BUNDLE_PRODUCT_ID
    else:
        product_id = settings.VPN_PRODUCT_ID

    available_plans = _vpn_get_available_plans(country_code, lang, bundle_relay)
    selected_plan = available_plans.get(plan, VPN_12_MONTH_PLAN)
    plan_id = selected_plan.get("id")

    product_url = f"{settings.VPN_SUBSCRIPTION_URL}subscriptions/products/{product_id}?plan={plan_id}"

    if "analytics" in selected_plan:
        if class_name is None:
            class_name = ""
        class_name += " ga-begin-checkout"
        if optional_attributes is None:
            optional_attributes = {}
        optional_attributes["data-ga-item"] = _vpn_get_ga_data(selected_plan)

    return _vpn_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)


@library.global_function
@jinja2.pass_context
def vpn_monthly_price(ctx, plan=VPN_12_MONTH_PLAN, country_code=None, lang=None, bundle_relay=False):
    """
    Render a localized string displaying VPN monthly plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_monthly_price(country_code=country_code,
                             lang=LANG) }}
    """

    available_plans = _vpn_get_available_plans(country_code, lang, bundle_relay)
    selected_plan = available_plans.get(plan, VPN_12_MONTH_PLAN)
    price = selected_plan.get("price")
    currency = selected_plan.get("currency")
    currency_locale = lang.replace("-", "_")
    amount = _format_currency(price, currency, currency_locale)

    if country_code in TAX_NOT_INCLUDED:
        price = ftl("vpn-shared-pricing-monthly-plus-tax", fallback="vpn-shared-pricing-monthly", amount=amount, ftl_files=FTL_FILES)
    else:
        price = ftl("vpn-shared-pricing-monthly", amount=amount, ftl_files=FTL_FILES)

    markup = f'<span class="vpn-monthly-price-display">{price}</span>'

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def vpn_total_price(ctx, country_code=None, lang=None, bundle_relay=False):
    """
    Render a localized string displaying VPN total plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_total_price(country_code=country_code, lang=LANG) }}
    """

    available_plans = _vpn_get_available_plans(country_code, lang, bundle_relay)
    selected_plan = available_plans.get(VPN_12_MONTH_PLAN)
    price = selected_plan.get("total")
    currency = selected_plan.get("currency")
    currency_locale = lang.replace("-", "_")
    amount = _format_currency(price, currency, currency_locale)

    if country_code in TAX_NOT_INCLUDED:
        price = ftl("vpn-shared-pricing-total-plus-tax", fallback="vpn-shared-pricing-total", amount=amount, ftl_files=FTL_FILES)
    else:
        price = ftl("vpn-shared-pricing-total", amount=amount, ftl_files=FTL_FILES)

    markup = price

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def vpn_saving(ctx, country_code=None, lang=None, bundle_relay=False, ftl_string="vpn-shared-pricing-save-percent"):
    """
    Render a localized string displaying saving (as a percentage) of a given VPN subscription plan.

    Examples
    ========

    In Template
    -----------

        {{ vpn_saving(country_code=country_code, lang=LANG) }}
    """

    available_plans = _vpn_get_available_plans(country_code, lang, bundle_relay)
    selected_plan = available_plans.get(VPN_12_MONTH_PLAN)
    percent = selected_plan.get("saving")
    saving = ftl(ftl_string, percent=percent, ftl_files=FTL_FILES)

    markup = saving

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def vpn_product_referral_link(
    ctx,
    referral_id="",
    link_to_pricing_page=False,
    page_anchor="",
    link_text=None,
    class_name=None,
    optional_attributes=None,
    optional_parameters=None,
):
    """
    Render link to the /products/vpn/ landing page with referral attribution markup

    Examples
    ========

    In Template
    -----------

        {{ vpn_product_referral_link(referral_id='navigation', link_text='Get Mozilla VPN') }}
    """

    href = reverse("products.vpn.pricing") if link_to_pricing_page else reverse("products.vpn.landing")
    css_class = "mzp-c-button js-fxa-product-referral-link"
    attrs = f'data-referral-id="{referral_id}" '

    if optional_attributes:
        attrs += " ".join(f'{attr}="{val}"' for attr, val in optional_attributes.items())

    if optional_parameters:
        params = "&".join(f"{param}={val}" for param, val in optional_parameters.items())
        href += f"?{params}"

    if class_name:
        css_class += f" {class_name}"

    markup = f'<a href="{href}{page_anchor}" class="{css_class}" {attrs}>{link_text}</a>'

    return Markup(markup)


# RELAY ================================================================

RELAY_MONTH_PLAN = "monthly"
RELAY_12_MONTH_PLAN = "monthly_when_yearly"
RELAY_PRODUCT = "relay-email"


@library.global_function
def relay_free_addresses():
    return settings.RELAY_MAX_NUM_FREE_ALIASES


@library.global_function
def relay_bundle_servers():
    return settings.VPN_CONNECT_SERVERS


@library.global_function
def relay_bundle_countries():
    return settings.VPN_CONNECT_COUNTRIES


def _relay_make_ga_data(id, product, country_code, lang, plan):
    plan = RELAY_MONTH_PLAN if plan == RELAY_MONTH_PLAN else RELAY_12_MONTH_PLAN
    currency = _relay_get_currency(product, country_code, lang)
    if product == "relay-bundle":
        # the bundle doesn't have a monthly price, discount calculated in reverse from % savings
        yearly_when_yearly = relay_monthly_price("relay-bundle", RELAY_12_MONTH_PLAN, country_code, lang) * 12
        discount = 55.92
    else:
        monthly_when_monthly = relay_monthly_price(product, RELAY_MONTH_PLAN, country_code, lang)
        monthly_when_yearly = relay_monthly_price(product, RELAY_12_MONTH_PLAN, country_code, lang)
        yearly_when_yearly = monthly_when_yearly * 12
        discount = 0 if plan == RELAY_MONTH_PLAN else ((monthly_when_monthly - monthly_when_yearly) * 12)
    price = monthly_when_monthly if plan == RELAY_MONTH_PLAN else float(yearly_when_yearly)

    ga_data = (
        f"{{'id' : '{id}', 'brand' : 'relay', 'plan' : '{product}', 'period' : '{'monthly' if plan == 'monthly' else 'yearly'}', "
        f"'price' : '{price:.2f}', 'discount' : '{discount:.2f}', 'currency' : '{currency}'}}"
    )

    return ga_data


def _relay_get_region(product, country_code, lang):
    """
    Return the "region" code for this request
    """

    lang = lang.split("-")[0]  # i.e. if it's en-US we only want the en part

    product = product.replace("relay-", "")
    region_langs = settings.RELAY_PLANS_BY_COUNTRY_AND_LANGUAGE[product].get(country_code)

    # get region that matches requested language, or get first region
    region = region_langs.get(lang, list(region_langs.values())[0])

    return region


def _relay_get_product_region_dict(product, region):
    """
    Return a dict for the product's region, containing stripe IDs and currency
    """

    product = product.replace("relay-", "")
    product_region_dict = settings.RELAY_STRIPE_PLAN_DATA[product]["countries_and_regions"][region]

    return product_region_dict


def _relay_get_plan_id(product, country_code, lang, plan):
    """
    Return Stripe Plan ID for matching country, language, plan
    """

    region = _relay_get_region(product, country_code, lang)
    dict = _relay_get_product_region_dict(product, region)
    plan = "monthly_id" if plan == RELAY_MONTH_PLAN else "yearly_id"

    return dict[plan]


def _relay_get_currency(product, country_code, lang):
    region = _relay_get_region(product, country_code, lang)
    product_region = _relay_get_product_region_dict(product, region)

    return product_region["currency"]


def relay_monthly_price(product, plan, country_code, lang):
    """
    Return a number for monthly cost of matching country, language, plan
    """
    plan = RELAY_MONTH_PLAN if plan == RELAY_MONTH_PLAN else RELAY_12_MONTH_PLAN
    currency = _relay_get_currency(product, country_code, lang)
    product = product.replace("relay-", "")

    price = settings.RELAY_STRIPE_PLAN_DATA[product]["prices"][currency][plan]
    price = Decimal(price)

    return price


def _relay_product_link(product_url, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
    separator = "&" if "?" in product_url else "?"
    client_id = settings.RELAY_CLIENT_ID
    href = f"{product_url}{separator}entrypoint={entrypoint}&form_type=button&service={client_id}&utm_source={entrypoint}&utm_medium=referral"

    if optional_parameters:
        params = "&".join(f"{param}={val}" for param, val in optional_parameters.items())
        href += f"&{params}"

    css_class = "js-fxa-product-cta-link js-fxa-product-button"
    attrs = ""

    if optional_attributes:
        attrs += " ".join(f'{attr}="{val}"' for attr, val in optional_attributes.items())

        # If there's a `data-cta-position` attribute for GA, also pass that as a query param
        position = optional_attributes.get("data-cta-position", None)

        if position:
            href += f"&data_cta_position={position}"

    if class_name:
        css_class += f" {class_name}"

    markup = f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>' f"{link_text}" f"</a>"

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def relay_subscribe_link(
    ctx,
    entrypoint,
    link_text,
    product="relay-email",
    plan=RELAY_12_MONTH_PLAN,
    class_name=None,
    country_code=None,
    lang=None,
    optional_parameters=None,
    optional_attributes=None,
):
    """
    Render a Relay subscribe link with required params for FxA authentication.

    Examples
    ========

    In Template
    -----------

        {{ relay_subscribe_link(
            entrypoint=_utm_source,
            link_text=ftl('plan-matrix-sign-up'),
            product='relay-email',
            plan='monthly',
            class_name='mzp-c-button mzp-t-product mzp-t-lg c-matrix-footer-button c-matrix-footer-button-monthly',
            country_code=country_code,
            lang=LANG,
            optional_parameters={
                'utm_campaign': _utm_campaign
            },
            optional_attributes={
                'data-cta-type': 'fxa-relay',
                'data-cta-position': 'matrix'
            })
        }}
    """

    if product == "relay-email":
        product_id = settings.RELAY_EMAIL_PRODUCT_ID
    elif product == "relay-phone":
        product_id = settings.RELAY_PHONE_PRODUCT_ID
    elif product == "relay-bundle":
        product_id = settings.RELAY_VPN_BUNDLE_PRODUCT_ID
    else:
        raise Exception("Unrecognized product passed to relay_subscribe_link()")

    plan_id = _relay_get_plan_id(product, country_code, lang, plan)

    product_url = f"{settings.RELAY_SUBSCRIPTION_URL}subscriptions/products/{product_id}?plan={plan_id}"

    # analytics data
    if class_name is None:
        class_name = ""
    class_name += " ga-begin-checkout"
    if optional_attributes is None:
        optional_attributes = {}
    optional_attributes["data-ga-item"] = _relay_make_ga_data(plan_id, product, country_code, lang, plan)

    return _relay_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)


@library.global_function
def relay_monthly_price_formatted(product=RELAY_PRODUCT, plan=RELAY_12_MONTH_PLAN, country_code=None, lang=None):
    """
    Render a localized string displaying a Relay plan's monthly plan.

    Examples
    ========

    In Template
    -----------

        {{ relay_monthly_price_formatted( product='relay-email',
                             country_code=country_code,
                             lang=LANG,
                            ) }}

    Output
    -----------

        country_code=CA, lang=en-CA => US$0.99/mo.
        country_code=DE, lang=de => 0,99 €/Monat

    """

    currency = _relay_get_currency(product, country_code, lang)
    amount = relay_monthly_price(product, plan, country_code, lang)
    currency_locale = lang.replace("-", "_")
    price = _format_currency(amount, currency, currency_locale)

    return Markup(price)


@library.global_function
def relay_bundle_savings():
    """
    The VPN/Relay bundle savings as a number representing a percent. Example: 50

    Examples
    ========

    In Template
    -----------

        {{ relay_bundle_savings(country_code=country_code, lang=LANG) }}
    """

    # there's only one supported region
    savings = settings.RELAY_STRIPE_PLAN_DATA["bundle"]["prices"]["USD"]["saving"]

    return Markup(savings)
