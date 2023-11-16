---
title: Using External Content Cards Data
---

The [www-admin repo](https://www-admin.readthedocs.io/) contains data
files and images that are synced to bedrock and available for use on any
page. The docs for updating said data is available via that repo, but
this page will explain how to use the cards data once it's in the
bedrock database.

# Add to a View

The easiest way to make the data available to a page is to add the
`page_content_cards` variable to the template context:

``` python
from bedrock.contentcards.models import get_page_content_cards

def view_with_cards(request):
    locale = l10n_utils.get_locale(request)
    ctx = {'page_content_cards': get_page_content_cards('home', locale)}
    return l10n_utils.render(request, 'sweet-words.html', ctx)
```

The `get_page_content_cards` returns a dict of card data dicts for the
given page (`home` in this case) and locale. The dict keys are the names
of the cards (e.g. `card_1`). If the `page_content_cards` context
variable is available in the template, then the `content_card()` macro
will discover it automatically.

!!! note

    The `get_page_content_cards` function is not all that clever as far as
    l10n is concerned. If you have translated the cards in the www-admin
    repo that is great, but you should have cards for every locale for which
    the page is active or the function will return an empty dict. This is
    especially tricky if you have multiple English locales enabled (en-US,
    en-CA, en-GB, etc.) and want the same cards to be used for all of them.
    You'd need to do something like `if locale.startswith('en-'):` then use
    `en-US` in the function call.

    Alternately you could just wrap the section of the template using cards
    to be optional in an `{% if page_content_cards %}` statement, and that
    way it will not show the section at all if the dict is empty if there
    are no cards for that page and locale combination.

# Add to the Template

Once you have the data in the template context, using a card is simple:

``` jinja
{% from "macros-protocol.html" import content_card with context %}

{{ content_card('card_1') }}
```

This will insert the data from the `card_1.en-US.md` file from the
www-admin repo into the template via the `card()` macro normally used
for protocol content cards.

If you don't have the `page_content_cards` variable in the template
context and you don't want to create or modify a view, you can fetch
the cards via a helper function in the template itself, but you have to
pass the result to the macro:

``` jinja
{% from "macros-protocol.html" import content_card with context %}
{% set content_cards = get_page_content_cards('home', LANG) %}

{{ content_card('card_1', content_cards) }}
```
