# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from html import escape

import basket
import basket.errors
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_safe

from bedrock.newsletter.views import general_error, invalid_email_address
from bedrock.products.forms import VPNWaitlistForm
from lib import l10n_utils
from lib.l10n_utils.fluent import ftl


VPN_FIXED_MONTHLY_PRICE = 'US$4.99'
VPN_VARIABLE_MONTHLY_PRICE = '9,99‎ €'
VPN_VARIABLE_6_MONTH_PRICE = '6,99 €'
VPN_VARIABLE_12_MONTH_PRICE = '4,99 €'
VPN_VARIABLE_6_MONTH_PRICE_TOTAL = '41,94 €'
VPN_VARIABLE_12_MONTH_PRICE_TOTAL = '59,88 €'
VPN_AVAILABLE_COUNTRIES = 6
VPN_CONNECT_SERVERS = 750
VPN_CONNECT_COUNTRIES = 30
VPN_CONNECT_DEVICES = 5


def vpn_fixed_price_countries():
    countries = settings.VPN_FIXED_PRICE_COUNTRY_CODES
    return '|%s|' % '|'.join(cc.lower() for cc in countries)


@require_safe
def vpn_landing_page(request):
    ftl_files = ['products/vpn/landing', 'products/vpn/shared']

    locale = l10n_utils.get_locale(request)
    sub_not_found = request.GET.get('vpn-sub-not-found', None)
    entrypoint_experiment = request.GET.get('entrypoint_experiment', None)
    entrypoint_variation = request.GET.get('entrypoint_variation', None)

    # error message for visitors who try to sign-in without a subscription (issue 10002)
    if sub_not_found == 'true':
        sub_not_found = True
    else:
        sub_not_found = False

    # ensure experiment parameters matches pre-defined values
    if entrypoint_variation not in ['a', 'b', 'c', 'd']:
        entrypoint_variation = None

    if entrypoint_experiment != 'vpn-landing-page-heading':
        entrypoint_variation = None

    if entrypoint_experiment and entrypoint_variation and locale in ['en-US', 'de', 'fr']:
        template_name = 'products/vpn/variants/heading-{}.html'.format(entrypoint_variation)
    else:
        template_name = 'products/vpn/landing.html'

    context = {
        'fixed_price_countries': vpn_fixed_price_countries(),
        'fixed_monthly_price': VPN_FIXED_MONTHLY_PRICE,
        'variable_monthly_price': VPN_VARIABLE_MONTHLY_PRICE,
        'variable_6_month_price': VPN_VARIABLE_6_MONTH_PRICE,
        'variable_12_month_price': VPN_VARIABLE_12_MONTH_PRICE,
        'variable_6_month_price_total': VPN_VARIABLE_6_MONTH_PRICE_TOTAL,
        'variable_12_month_price_total': VPN_VARIABLE_12_MONTH_PRICE_TOTAL,
        'available_countries': VPN_AVAILABLE_COUNTRIES,
        'connect_servers': VPN_CONNECT_SERVERS,
        'connect_countries': VPN_CONNECT_COUNTRIES,
        'connect_devices': VPN_CONNECT_DEVICES,
        'sub_not_found': sub_not_found
    }

    return l10n_utils.render(request, template_name, context, ftl_files=ftl_files)


@require_safe
def vpn_invite_page(request):
    ftl_files = ['products/vpn/landing', 'products/vpn/shared']
    locale = l10n_utils.get_locale(request)
    newsletter_form = VPNWaitlistForm(locale)

    return l10n_utils.render(
        request, 'products/vpn/invite.html', {'newsletter_form': newsletter_form}, ftl_files=ftl_files
    )


@require_POST
def vpn_invite_waitlist(request):
    errors = []
    locale = l10n_utils.get_locale(request)
    form = VPNWaitlistForm(locale, request.POST)
    if form.is_valid():
        data = form.cleaned_data
        kwargs = {
            'email': data['email'],
            'fpn_platform': ','.join(data['platforms']),
            'fpn_country': data['country'],
            'lang': data['lang'],
            'newsletters': 'guardian-vpn-waitlist',
        }
        if settings.BASKET_API_KEY:
            kwargs['api_key'] = settings.BASKET_API_KEY

        # NOTE this is not a typo; Referrer is misspelled in the HTTP spec
        # https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.36
        if not kwargs.get('source_url') and request.META.get('HTTP_REFERER'):
            kwargs['source_url'] = request.META['HTTP_REFERER']

        try:
            basket.subscribe(**kwargs)
        except basket.BasketException as e:
            if e.code == basket.errors.BASKET_INVALID_EMAIL:
                errors.append(str(invalid_email_address))
            else:
                errors.append(str(general_error))
    else:
        if 'email' in form.errors:
            errors.append(ftl('newsletter-form-please-enter-a-valid'))
        if 'privacy' in form.errors:
            errors.append(ftl('newsletter-form-you-must-agree-to'))
        for fieldname in ('fmt', 'lang', 'country'):
            if fieldname in form.errors:
                errors.extend(form.errors[fieldname])

    if errors:
        errors = [escape(e) for e in errors]
        resp = {
            'success': False,
            'errors': errors,
        }
    else:
        resp = {'success': True}

    return JsonResponse(resp)
