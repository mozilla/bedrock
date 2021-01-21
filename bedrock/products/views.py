# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils
from django.conf import settings

from bedrock.newsletter.forms import NewsletterFooterForm


def vpn_monthly_price(locale):
    try:
        price = settings.VPN_PRICE_MONTHLY[locale]['monthly']
    except KeyError:
        price = settings.VPN_PRICE_MONTHLY['en-US']['monthly']
    return price


def vpn_allowed_countries():
    countries = settings.VPN_ALLOWED_COUNTRY_CODES
    return '|%s|' % '|'.join(cc.lower() for cc in countries)


def vpn_landing_page(request):
    locale = l10n_utils.get_locale(request)
    template_name = 'products/vpn/landing.html'

    context = {
        'allowed_countries': vpn_allowed_countries(),
        'monthly_price': vpn_monthly_price(locale),

    }

    return l10n_utils.render(request, template_name, context,
                             ftl_files=[])


def vpn_invite_page(request):
    locale = l10n_utils.get_locale(request)
    newsletter_form = NewsletterFooterForm('guardian-vpn-waitlist', locale)

    return l10n_utils.render(
        request, 'products/vpn/invite.html', {'newsletter_form': newsletter_form}
    )
