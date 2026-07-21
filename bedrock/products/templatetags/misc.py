# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
    analytics = selected_plan.get("analytics")

    ga_data = (
        f"{{"
        f"'brand' : '{analytics.get('brand')}',"
        f"'plan' : '{analytics.get('plan')}',"
        f"'period' : '{analytics.get('period')}',"
        f"'price' : '{analytics.get('price')}',"
        f"'discount' : '{analytics.get('discount')}',"
        f"'currency' : '{analytics.get('currency')}'"
        f"}}"
    )

    return ga_data


def _vpn_get_available_plans(country_code, lang):
    """
    Get subscription plan IDs using country_code and page language.
    Defaults to "US" if no matching country code is found.
    Each country also has a default language if no match is found.
    """

    country_plans = settings.VPN_VARIABLE_PRICING.get(country_code, settings.VPN_VARIABLE_PRICING["US"])

    return country_plans.get(lang, country_plans.get("default"))


def _vpn_get_mobile_plans(country_code):
    """
    Get mobile only subscription plans using country_code.
    Defaults to "US" if no matching country code is found.
    """

    return settings.VPN_MOBILE_SUB_PRICING.get(country_code, settings.VPN_MOBILE_SUB_PRICING["US"])


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

    markup = f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>{link_text}</a>'

    return Markup(markup)


@library.global_function
def vpn_supported_locale(LANG):
    """
    Global helper that can be passed locale via a template
    in order to determine if the VPN app is translated
    in a visitor's language.
    """
    locale = LANG.split("-")[0]

    return locale in settings.VPN_SUPPORTED_LOCALES


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

    product_id = settings.VPN_PRODUCT_ID

    available_plans = _vpn_get_available_plans(country_code, lang)
    selected_plan = available_plans.get(plan, VPN_12_MONTH_PLAN)

    product_id = settings.VPN_PRODUCT_ID_NEXT
    plan_slug = "yearly" if plan == VPN_12_MONTH_PLAN else "monthly"

    # For testing/QA we support a test 'daily' API endpoint on the staging API only
    # We only want to override the monthly VPN option when in QA mode; annual remains unchanged
    # https://mozilla-hub.atlassian.net/browse/VPN-6985
    if plan_slug == "monthly" and settings.VPN_SUBSCRIPTION_USE_DAILY_MODE__QA_ONLY:
        plan_slug = "daily"

    product_url = f"{settings.VPN_SUBSCRIPTION_URL_NEXT}{product_id}/{plan_slug}/landing/"

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
def vpn_monthly_price(ctx, plan=VPN_12_MONTH_PLAN, country_code=None, lang=None):
    """
    Render a localized string displaying VPN monthly plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_monthly_price(country_code=country_code,
                             lang=LANG) }}
    """

    available_plans = _vpn_get_available_plans(country_code, lang)
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
def vpn_mobile_monthly_price(ctx, plan=VPN_12_MONTH_PLAN, country_code=None, lang=None):
    """
    Render a localized string displaying VPN monthly plan price for a mobile subscription.
    This is used for countries where a VPN subscription can only be purchased through the
    Google Play Store or the Apple App Store, and uses a different pricing plan matrix to
    countries that purchase through FxA / sub-plat.

    Examples
    ========

    In Template
    -----------

        {{ vpn_mobile_monthly_price(country_code=country_code, lang=LANG) }}
    """

    available_plans = _vpn_get_mobile_plans(country_code)
    selected_plan = available_plans.get(plan, VPN_12_MONTH_PLAN)
    price = selected_plan.get("price")
    currency = selected_plan.get("currency")
    currency_locale = lang.replace("-", "_")
    amount = _format_currency(price, currency, currency_locale)
    price = ftl("vpn-shared-pricing-monthly", amount=amount, ftl_files=FTL_FILES)

    markup = f'<span class="vpn-monthly-price-display">{price}</span>'

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def vpn_total_price(ctx, country_code=None, lang=None):
    """
    Render a localized string displaying VPN total plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_total_price(country_code=country_code, lang=LANG) }}
    """

    available_plans = _vpn_get_available_plans(country_code, lang)
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
def vpn_mobile_total_price(ctx, country_code=None, lang=None):
    """
    Render a localized string displaying VPN total plan price for a mobile subscription.
    This is used for countries where a VPN subscription can only be purchased through the
    Google Play Store or the Apple App Store, and uses a different pricing plan matrix to
    countries that purchase through FxA / sub-plat.

    Examples
    ========

    In Template
    -----------

        {{ vpn_mobile_total_price(country_code=country_code, lang=LANG) }}
    """

    available_plans = _vpn_get_mobile_plans(country_code)
    selected_plan = available_plans.get(VPN_12_MONTH_PLAN)
    price = selected_plan.get("total")
    currency = selected_plan.get("currency")
    currency_locale = lang.replace("-", "_")
    amount = _format_currency(price, currency, currency_locale)
    price = ftl("vpn-shared-pricing-total", amount=amount, ftl_files=FTL_FILES)

    markup = price

    return Markup(markup)


@library.global_function
@jinja2.pass_context
def vpn_saving(ctx, country_code=None, lang=None, ftl_string="vpn-shared-pricing-save-percent"):
    """
    Render a localized string displaying saving (as a percentage) of a given VPN subscription plan.

    Examples
    ========

    In Template
    -----------

        {{ vpn_saving(country_code=country_code, lang=LANG) }}
    """

    available_plans = _vpn_get_available_plans(country_code, lang)
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
    is_cta_button_styled=True,
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
    css_class = "mzp-c-button js-fxa-product-referral-link" if is_cta_button_styled else "js-fxa-product-referral-link"
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
