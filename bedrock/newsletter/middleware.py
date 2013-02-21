import basket
from lib.l10n_utils.dotlang import _lazy
from bedrock.newsletter.forms import NewsletterFooterForm


class NewsletterMiddleware(object):
    """Processes newsletter subscriptions"""
    def process_request(self, request):
        success = False
        form = NewsletterFooterForm(request.locale, request.POST or None)

        is_footer_form = (request.method == 'POST' and
                          'newsletter-footer' in request.POST)
        if is_footer_form:
            if form.is_valid():
                data = form.cleaned_data
                kwargs = {
                    'format': data['fmt'],
                }
                # add optional data
                kwargs.update(dict((k, data[k]) for k in ['country',
                                                          'lang',
                                                          'source_url']
                                   if data[k]))
                try:
                    basket.subscribe(data['email'], data['newsletter'],
                                     **kwargs)
                    success = True
                except basket.BasketException:
                    msg = _lazy("We are sorry, but there was a problem "
                                "with our system. Please try again later!")
                    form.errors['__all__'] = form.error_class([msg])

        request.newsletter_form = form
        request.newsletter_success = success
