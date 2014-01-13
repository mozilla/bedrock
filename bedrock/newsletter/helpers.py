# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

import basket
import jingo
import jinja2

from lib.l10n_utils import get_locale
from lib.l10n_utils.dotlang import _lazy
from bedrock.newsletter.forms import NewsletterFooterForm


log = logging.getLogger(__name__)


@jingo.register.function
@jinja2.contextfunction
def email_newsletter_form(ctx, newsletters='mozilla-and-you', title=None,
                          include_country=True, include_language=True,
                          use_thankyou=True, footer=True, process_form=True):
    request = ctx['request']
    context = ctx.get_all()
    context.update(dict(
        id=newsletters,
        title=title,
        include_country=include_country,
        include_language=include_language,
        use_thankyou=use_thankyou,
        footer=footer,
    ))
    success = False
    form = NewsletterFooterForm(newsletters, get_locale(request),
                                request.POST or None)

    if process_form and request.method == 'POST':
        if form.is_valid():
            data = form.cleaned_data

            # If data['lang'] is set, pass it to the template.
            # If it's None, empty, or nonexistent, pass 'en'.
            context['lang'] = data.get('lang', 'en').strip() or 'en'

            kwargs = {'format': data['fmt']}
            # add optional data
            kwargs.update(dict((k, data[k]) for k in ['country',
                                                      'lang',
                                                      'source_url']
                               if data[k]))
            try:
                basket.subscribe(data['email'], form.newsletters,
                                 **kwargs)
            except basket.BasketException:
                log.exception("Error subscribing %s to newsletter %s" %
                              (data['email'], newsletters))
                msg = _lazy("We are sorry, but there was a problem "
                            "with our system. Please try again later!")
                form.errors['__all__'] = form.error_class([msg])
            else:
                success = True

    request.newsletter_success = success
    context.update(dict(form=form, success=success))
    html = jingo.render_to_string(request, 'newsletter/includes/form.html', context)
    if not (success and not use_thankyou):
        return jinja2.Markup(html)
