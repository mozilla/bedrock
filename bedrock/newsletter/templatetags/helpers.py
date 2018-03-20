# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

import jinja2
from django.template.loader import render_to_string
from django_jinja import library

from lib.l10n_utils import get_locale
from bedrock.newsletter.forms import NewsletterFooterForm


log = logging.getLogger(__name__)


@library.global_function
@jinja2.contextfunction
def email_newsletter_form(ctx, newsletters='mozilla-and-you', title=None,
                          subtitle=None, include_country=True,
                          include_language=True, details=None,
                          use_thankyou=True, thankyou_head=None,
                          thankyou_content=None, footer=True,
                          process_form=True, include_title=None,
                          submit_text=None, button_class=None,
                          email_placeholder=None, email_label=None,
                          spinner_color=None):
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
        subtitle=subtitle,  # nested in/depends on include_title
        include_country=include_country,
        include_language=include_language,
        details=details,
        use_thankyou=use_thankyou,
        thankyou_head=thankyou_head,
        thankyou_content=thankyou_content,
        footer=footer,
        include_title=include_title if include_title is not None else footer,
        form=form,
        submit_text=submit_text,
        button_class=button_class,
        spinner_color=spinner_color,
        email_placeholder=email_placeholder,
        email_label=email_label,
        success=success,
    ))

    html = render_to_string('newsletter/includes/form.html', context, request=request)
    return jinja2.Markup(html)
