# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django_jinja import library

from bedrock.contentcards.models import ContentCard


@library.global_function
def get_content_card(page_cards, name):
    # page_cards is a dict of card_name to card_data
    return page_cards.get(name)


@library.global_function
def get_page_content_cards(page_name, locale):
    return ContentCard.objects.get_page_cards(page_name, locale)
