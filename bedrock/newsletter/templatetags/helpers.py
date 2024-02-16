# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from django.conf import settings
from django.template.loader import render_to_string

import jinja2
from django_jinja import library
from markupsafe import Markup

from bedrock.newsletter.forms import NewsletterFooterForm
from lib.l10n_utils import get_locale

log = logging.getLogger(__name__)


@library.global_function
@jinja2.pass_context
def email_newsletter_form(
    ctx,
    newsletters="mozilla-and-you",
    title=None,
    subtitle=None,
    desc=None,
    include_country=True,
    include_language=True,
    details=None,
    use_thankyou=True,
    thankyou_head=None,
    thankyou_content=None,
    footer=True,
    include_title=None,
    submit_text=None,
    button_class=None,
    spinner_color=None,
    email_label=None,
    email_placeholder=None,
):
    request = ctx["request"]
    context = ctx.get_all()
    action = settings.BASKET_SUBSCRIBE_URL

    success = bool(ctx.get("success"))
    if success and not use_thankyou:
        return

    form = ctx.get("newsletter_form", None)
    if not form:
        form = NewsletterFooterForm(newsletters, get_locale(request))

    if isinstance(newsletters, list):
        newsletters = ", ".join(newsletters)

    is_multi_newsletter = "," in newsletters

    context.update(
        dict(
            id="mozilla-firefox-multi" if is_multi_newsletter else newsletters,
            title=title,
            subtitle=subtitle,  # nested in/depends on include_title
            desc=desc,  # nested in/depends on include_title
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
            success=success,
            email_label=email_label,
            email_placeholder=email_placeholder,
            is_multi_newsletter_form=is_multi_newsletter,
            action=action,
        )
    )

    html = render_to_string("newsletter/includes/form.html", context, request=request)
    return Markup(html)
