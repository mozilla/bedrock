# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

from bedrock.legal_docs.models import LegalDoc
from lib import l10n_utils


CACHE_TIMEOUT = settings.LEGAL_DOCS_CACHE_TIMEOUT


def load_legal_doc(doc_name, locale):
    """
    Return the HTML content of a legal doc in the requested locale.

    :param doc_name: name of the legal doc folder
    :param locale: preferred language version of the doc
    :return: dict containing string content of the file (or None), a boolean
             value indicating whether the file is localized into the specified
             locale, and a dict of all available locales for that document
    """
    try:
        doc = LegalDoc.objects.get_doc(doc_name, locale)
    except LegalDoc.DoesNotExist:
        try:
            doc = LegalDoc.objects.get_doc(doc_name, 'en')
        except LegalDoc.DoesNotExist:
            try:
                doc = LegalDoc.objects.get_doc(doc_name, 'en-US')
            except LegalDoc.DoesNotExist:
                doc = None

    return doc


class LegalDocView(TemplateView):
    """
    Generic view for loading a legal doc and displaying it with a template.

    Class attributes in addition to standard Django TemplateView:

    * legal_doc_name: The name of the folder in the legal_docs repo.
    * legal_doc_context_name: (default 'doc') template variable name for legal doc.

    This view automatically adds the `cache_page` decorator. The default timeout
    is 10 minutes, configurable by setting the `LEGAL_DOCS_CACHE_TIMEOUT` setting to change
    the default for all views, or the `cache_timeout` property for an single instance.

    See `bedrock/privacy/views.py` for usage examples.
    """
    legal_doc_name = None
    legal_doc_context_name = 'doc'
    cache_timeout = CACHE_TIMEOUT

    def get_legal_doc(self):
        locale = l10n_utils.get_locale(self.request)
        return load_legal_doc(self.legal_doc_name, locale)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault('content_type', self.content_type)
        return l10n_utils.render(self.request,
                                 self.get_template_names()[0],
                                 context, **response_kwargs)

    def get_context_data(self, **kwargs):
        legal_doc = self.get_legal_doc()
        if legal_doc is None:
            raise Http404('Legal doc not found')

        context = super(LegalDocView, self).get_context_data(**kwargs)
        context[self.legal_doc_context_name] = legal_doc['content']
        context['active_locales'] = legal_doc['active_locales']
        return context

    @classmethod
    def as_view(cls, **initkwargs):
        cache_timeout = initkwargs.pop('cache_timeout', cls.cache_timeout)
        return cache_page(cache_timeout)(super(LegalDocView, cls).as_view(**initkwargs))
