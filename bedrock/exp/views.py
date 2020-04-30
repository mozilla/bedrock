# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from lib import l10n_utils
from django.conf import settings

from bedrock.contentcards.models import get_page_content_cards
from bedrock.pocketfeed.models import PocketArticle


def new(request):

    # note: v and xv params only allow a-z, A-Z, 0-9, -, and _ characters
    experience = request.GET.get('xv', None)
    variant = request.GET.get('v', None)

    # ensure experience matches pre-defined value
    if experience not in ['']:  # place expected ?xv= values in this list
        experience = None

    # ensure variant matches pre-defined value
    if variant not in ['']:  # place expected ?v= values in this list
        variant = None

    # no harm done by passing 'v' to template, even when no experiment is running
    # (also makes tests easier to maintain by always sending a context)
    return l10n_utils.render(
        request, 'exp/firefox/new/download.html', {'experience': experience, 'v': variant, 'active_locales': ['en-US', 'en-GB', 'en-CA', 'de']}
    )


def home_view(request):
    locale = l10n_utils.get_locale(request)
    donate_params = settings.DONATE_PARAMS.get(
        locale, settings.DONATE_PARAMS['en-US'])

    # presets are stored as a string but, for the home banner
    # we need it as a list.
    donate_params['preset_list'] = donate_params['presets'].split(',')
    ctx = {
        'donate_params': donate_params,
        'pocket_articles': PocketArticle.objects.all()[:4],
        'active_locales': ['de', 'fr', 'en-US']
    }

    if locale.startswith('en-'):
        template_name = 'exp/home/home-en.html'
        ctx['page_content_cards'] = get_page_content_cards('home-2019', 'en-US')
    elif locale == 'de':
        template_name = 'exp/home/home-de.html'
        ctx['page_content_cards'] = get_page_content_cards('home-de', 'de')
    elif locale == 'fr':
        template_name = 'exp/home/home-fr.html'
        ctx['page_content_cards'] = get_page_content_cards('home-fr', 'fr')

    return l10n_utils.render(request, template_name, ctx)
