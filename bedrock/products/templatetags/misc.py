# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.conf import settings

import jinja2
from django_jinja import library

from bedrock.base.urlresolvers import reverse
from lib.l10n_utils.fluent import ftl

FTL_FILES = ["products/vpn/shared"]


def get_available_plans(country_code, lang):
    """
    Get subscription plan IDs using country_code and page language.
    Defaults to "US" if no matching country code is found.
    Each country also has a default language if no match is found.
    """
    country_plans = settings.VPN_VARIABLE_PRICING.get(country_code, settings.VPN_VARIABLE_PRICING["US"])
    return country_plans.get(lang, country_plans.get("default"))


def _vpn_product_link(product_url, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
    separator = "&" if "?" in product_url else "?"
    href = f"{product_url}{separator}entrypoint={entrypoint}&form_type=button&utm_source={entrypoint}&utm_medium=referral"

    if optional_parameters:
        params = "&".join("%s=%s" % (param, val) for param, val in optional_parameters.items())
        href += f"&{params}"

    css_class = "js-vpn-cta-link js-fxa-product-button"
    attrs = ""

    if optional_attributes:
        attrs += " ".join('%s="%s"' % (attr, val) for attr, val in optional_attributes.items())

        # If there's a `data-cta-position` attribute for GA, also pass that as a query param to vpn.m.o.
        position = optional_attributes.get("data-cta-position", None)

        if position:
            href += f"&data_cta_position={position}"

    if class_name:
        css_class += f" {class_name}"

    markup = f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>' f"{link_text}" f"</a>"

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def vpn_sign_in_link(ctx, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
    """
    Render a vpn.mozilla.org sign-in link with required params for FxA authentication.

    Examples
    ========

    In Template
    -----------

        {{ vpn_sign_in_link(entrypoint='www.mozilla.org-vpn-product-page', link_text='Sign In') }}
    """
    product_url = f"{settings.VPN_ENDPOINT}oauth/init"

    return _vpn_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)


@library.global_function
@jinja2.contextfunction
def vpn_subscribe_link(
    ctx, entrypoint, link_text, plan="12-month", class_name=None, country_code=None, lang=None, optional_parameters=None, optional_attributes=None
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

    available_plans = get_available_plans(country_code, lang)
    selected_plan = available_plans.get(plan)
    plan_id = selected_plan.get("id")

    product_url = f"{settings.VPN_SUBSCRIPTION_URL}subscriptions/products/{settings.VPN_PRODUCT_ID}?plan={plan_id}"

    return _vpn_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)


@library.global_function
@jinja2.contextfunction
def vpn_monthly_price(ctx, plan="monthly", country_code=None, lang=None):
    """
    Render a localized string displaying VPN monthly plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_monthly_price(plan='12-month',
                             country_code=country_code,
                             lang=LANG) }}
    """

    available_plans = get_available_plans(country_code, lang)
    selected_plan = available_plans.get(plan)
    amount = selected_plan.get("price")
    price = ftl("vpn-shared-pricing-monthly", amount=amount, ftl_files=FTL_FILES)

    markup = f'<span class="vpn-monthly-price-display">{price}</span>'

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def vpn_total_price(ctx, plan="12-month", country_code=None, lang=None):
    """
    Render a localized string displaying VPN total plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_total_price(plan='6-month',
                           country_code=country_code,
                           lang=LANG) }}
    """

    available_plans = get_available_plans(country_code, lang)
    selected_plan = available_plans.get(plan)
    amount = selected_plan.get("total")
    price = ftl("vpn-shared-pricing-total", amount=amount, ftl_files=FTL_FILES)

    markup = price

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def vpn_saving(ctx, plan="12-month", country_code=None, lang=None):
    """
    Render a localized string displaying saving (as a percentage) of a given VPN subscription plan.

    Examples
    ========

    In Template
    -----------

        {{ vpn_saving(plan='6-month',
                      country_code=country_code,
                      lang=LANG) }}
    """

    available_plans = get_available_plans(country_code, lang)
    selected_plan = available_plans.get(plan)
    percent = selected_plan.get("saving")
    saving = ftl("vpn-shared-pricing-save-percent", percent=percent, ftl_files=FTL_FILES)

    markup = saving

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def vpn_product_referral_link(ctx, referral_id="", page_anchor="", link_text=None, class_name=None, optional_attributes=None):
    """
    Render link to the /products/vpn/ landing page with referral attribution markup

    Examples
    ========

    In Template
    -----------

        {{ vpn_product_referral_link(referral_id='navigation', link_text='Get Mozilla VPN') }}
    """

    href = reverse("products.vpn.landing")
    css_class = "mzp-c-button mzp-t-product js-fxa-product-referral-link"
    attrs = f'data-referral-id="{referral_id}" '

    if optional_attributes:
        attrs += " ".join('%s="%s"' % (attr, val) for attr, val in optional_attributes.items())

    if class_name:
        css_class += f" {class_name}"

    markup = f'<a href="{href}{page_anchor}" class="{css_class}" {attrs}>{link_text}</a>'

    return jinja2.Markup(markup)
