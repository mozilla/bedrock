# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

import jingo
import jinja2

from lib.l10n_utils import get_locale
from bedrock.newsletter.forms import NewsletterFooterForm


log = logging.getLogger(__name__)


@jingo.register.function
@jinja2.contextfunction
def email_newsletter_form(ctx, newsletters='mozilla-and-you', title=None,
                          include_country=True, include_language=True,
                          use_thankyou=True, footer=True, process_form=True):
    request = ctx['request']
    context = ctx.get_all()

    success = bool(ctx.get('success'))
    if success and not use_thankyou:
        return

    form = ctx.get('newsletter_form', None)
    if not form:
        form = NewsletterFooterForm(newsletters, get_locale(request))

    context.update(dict(
        id=newsletters,
        title=title,
        include_country=include_country,
        include_language=include_language,
        use_thankyou=use_thankyou,
        footer=footer,
        form=form,
        success=success,
    ))

    html = jingo.render_to_string(request, 'newsletter/includes/form.html', context)
    return jinja2.Markup(html)
