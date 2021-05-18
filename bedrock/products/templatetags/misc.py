# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jinja2

from django.conf import settings
from django_jinja import library

from lib.l10n_utils.fluent import ftl

FTL_FILES = ['products/vpn/shared']


def _vpn_product_link(product_url, entrypoint, link_text, class_name=None, optional_parameters=None, optional_attributes=None):
    separator = '&' if '?' in product_url else '?'
    href = f'{product_url}{separator}entrypoint={entrypoint}&form_type=button&utm_source={entrypoint}&utm_medium=referral'

    if optional_parameters:
        params = '&'.join('%s=%s' % (param, val) for param, val in optional_parameters.items())
        href += f'&{params}'

    css_class = 'js-fxa-cta-link js-fxa-product-button'
    attrs = ''

    if optional_attributes:
        attrs += ' '.join('%s="%s"' % (attr, val) for attr, val in optional_attributes.items())

        # If there's a `data-cta-position` attribute for GA, also pass that as a query param to vpn.m.o.
        position = optional_attributes.get('data-cta-position', None)

        if position:
            href += f'&data_cta_position={position}'

    if class_name:
        css_class += f' {class_name}'

    markup = (f'<a href="{href}" data-action="{settings.FXA_ENDPOINT}" class="{css_class}" {attrs}>'
              f'{link_text}'
              f'</a>')

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
    product_url = f'{settings.VPN_ENDPOINT}oauth/init'

    return _vpn_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)


@library.global_function
@jinja2.contextfunction
def vpn_subscribe_link(ctx, entrypoint, link_text, plan=None, class_name=None, lang=None, optional_parameters=None, optional_attributes=None):
    """
    Render a vpn.mozilla.org subscribe link with required params for FxA authentication.

    Examples
    ========

    In Template
    -----------

        {{ vpn_subscribe_link(entrypoint='www.mozilla.org-vpn-product-page', link_text='Get Mozilla VPN') }}
    """

    # Subscription links currently support variable pricing in Euros for Germany and France only.
    if plan in ['12-month', '6-month', 'monthly']:

        # Set a default plan ID using page locale. This acts as a fallback should geo-location fail.
        pricing_params = settings.VPN_VARIABLE_PRICING.get(lang, settings.VPN_VARIABLE_PRICING['us'])
        plan_default = pricing_params[plan]['id']
        plan_attributes = {}

        # HTML data-attributes are used by client side JS to set the correct plan ID based on geo.
        for country in settings.VPN_VARIABLE_PRICING.items():
            plan_attributes.update({f'data-plan-{country[0]}': country[1][plan]['id']})

    # All other subscription links default to fixed monthly pricing in $US.
    else:
        plan_default = settings.VPN_FIXED_PRICE_MONTHLY_USD
        plan_attributes = None

    if (plan_attributes):
        optional_attributes = optional_attributes or {}
        optional_attributes.update(plan_attributes)

    product_url = f'{settings.VPN_ENDPOINT}r/vpn/subscribe/products/{settings.VPN_PRODUCT_ID}?plan={plan_default}'

    return _vpn_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)


@library.global_function
@jinja2.contextfunction
def vpn_monthly_price(ctx, plan='monthly', lang=None):
    """
    Render a localized string displaying VPN monthly plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_monthly_price(plan='12-month') }}
    """

    pricing_params = settings.VPN_VARIABLE_PRICING.get(lang, settings.VPN_VARIABLE_PRICING['us'])
    default_amount = pricing_params[plan]['price']
    euro_amount = settings.VPN_VARIABLE_PRICING['de'][plan]['price']
    usd_amount = settings.VPN_VARIABLE_PRICING['us'][plan]['price']
    default_text = ftl('vpn-shared-pricing-monthly', amount=default_amount, ftl_files=FTL_FILES)

    # HTML data-attributes are used by client side JS to set the correct display price based on geo.
    attributes = {
        'data-price-usd': ftl('vpn-shared-pricing-monthly', amount=usd_amount, ftl_files=FTL_FILES),
        'data-price-euro': ftl('vpn-shared-pricing-monthly', amount=euro_amount, ftl_files=FTL_FILES),
    }

    attrs = ' '.join('%s="%s"' % (attr, val) for attr, val in attributes.items())

    markup = (f'<span class="js-vpn-monthly-price-display" {attrs}>'
              f'{default_text}'
              f'</span>')

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def vpn_total_price(ctx, plan='12-month', lang=None):
    """
    Render a localized string displaying VPN total plan price.

    Examples
    ========

    In Template
    -----------

        {{ vpn_total_price(plan='6-month') }}
    """

    pricing_params = settings.VPN_VARIABLE_PRICING.get(lang, settings.VPN_VARIABLE_PRICING['us'])
    default_amount = pricing_params[plan]['total']
    euro_amount = settings.VPN_VARIABLE_PRICING['de'][plan]['total']
    usd_amount = settings.VPN_VARIABLE_PRICING['us'][plan]['total']
    default_text = ftl('vpn-shared-pricing-total', amount=default_amount, ftl_files=FTL_FILES)

    # HTML data-attributes are used by client side JS to set the correct display price based on geo.
    attributes = {
        'data-price-usd': ftl('vpn-shared-pricing-total', amount=usd_amount, ftl_files=FTL_FILES),
        'data-price-euro': ftl('vpn-shared-pricing-total', amount=euro_amount, ftl_files=FTL_FILES),
    }

    attrs = ' '.join('%s="%s"' % (attr, val) for attr, val in attributes.items())

    markup = (f'<span class="js-vpn-total-price-display" {attrs}>'
              f'{default_text}'
              f'</span>')

    return jinja2.Markup(markup)


@library.global_function
@jinja2.contextfunction
def vpn_saving(ctx, plan='12-month', lang=None):
    """
    Render a localized string displaying saving (as a percentage) of a given VPN subscription plan.

    Examples
    ========

    In Template
    -----------

        {{ vpn_saving(plan='6-month') }}
    """

    pricing_params = settings.VPN_VARIABLE_PRICING.get(lang, settings.VPN_VARIABLE_PRICING['us'])
    default_amount = pricing_params[plan]['saving']
    euro_amount = settings.VPN_VARIABLE_PRICING['de'][plan]['saving']
    usd_amount = settings.VPN_VARIABLE_PRICING['us'][plan]['saving']
    default_text = ftl('vpn-shared-pricing-save-percent', percent=default_amount, ftl_files=FTL_FILES)

    # HTML data-attributes are used by client side JS to set the correct saving based on geo.
    attributes = {
        'data-price-usd': ftl('vpn-shared-pricing-save-percent', percent=usd_amount, ftl_files=FTL_FILES),
        'data-price-euro': ftl('vpn-shared-pricing-save-percent', percent=euro_amount, ftl_files=FTL_FILES),
    }

    attrs = ' '.join('%s="%s"' % (attr, val) for attr, val in attributes.items())

    markup = (f'<span class="js-vpn-saving-display" {attrs}>'
              f'{default_text}'
              f'</span>')

    return jinja2.Markup(markup)
