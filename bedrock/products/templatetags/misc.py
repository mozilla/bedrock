# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import jinja2

from django.conf import settings
from django_jinja import library

from bedrock.base.waffle import switch


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

    # Switching to the new subscription URL format will be co-ordinated with the VPN product team (issue 10126).
    if switch('vpn-new-subscription-url-format'):

        # Subscription links currently support variable pricing in Euros for Germany and France only.
        if plan in ['12-month', '6-month', 'monthly']:

            # Set a default plan ID using page locale. This acts as a fallback should geo-location fail.
            if lang in ['de', 'fr']:
                plan_default = settings.VPN_VARIABLE_PRICING[lang][plan]
            else:
                plan_default = ''

            # HTML data-attributes are used by client side JS to set the correct plan ID based on geo.
            plan_attributes = {
                'data-plan-de': settings.VPN_VARIABLE_PRICING['de'][plan],
                'data-plan-fr': settings.VPN_VARIABLE_PRICING['fr'][plan]
            }
        # All other subscription links default to fixed monthly pricing in $US.
        else:
            plan_default = settings.VPN_FIXED_PRICE_MONTHLY_USD
            plan_attributes = None

        if (plan_attributes):
            optional_attributes = optional_attributes or {}
            optional_attributes.update(plan_attributes)

        product_url = f'{settings.VPN_ENDPOINT}r/vpn/subscribe/products/{settings.VPN_PRODUCT_ID}?plan={plan_default}'
    else:
        product_url = f'{settings.VPN_ENDPOINT}r/vpn/subscribe'

    return _vpn_product_link(product_url, entrypoint, link_text, class_name, optional_parameters, optional_attributes)
