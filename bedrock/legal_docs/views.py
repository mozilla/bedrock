# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os import path, listdir
import io

from django.conf import settings
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

import markdown as md
from mdx_outline import OutlineExtension

from bedrock.settings import path as base_path
from lib import l10n_utils

LEGAL_DOCS_PATH = base_path('vendor-local', 'src', 'legal-docs')
CACHE_TIMEOUT = getattr(settings, 'LEGAL_DOCS_CACHE_TIMEOUT', 60 * 60)
# legal-docs locales mapped to bedrock locales when they differ
# https://github.com/mozilla/bedrock/issues/6000
LEGAL_DOCS_LOCALES_TO_BEDROCK = {
    'hi': 'hi-IN',
}
BEDROCK_LOCALES_TO_LEGAL_DOCS = {v: k for k, v in list(LEGAL_DOCS_LOCALES_TO_BEDROCK.items())}


def load_legal_doc(doc_name, locale):
    """
    Return the HTML content of a legal doc in the requested locale.

    :param doc_name: name of the legal doc folder
    :param locale: preferred language version of the doc
    :return: dict containing string content of the file (or None), a boolean
             value indicating whether the file is localized into the specified
             locale, and a dict of all available locales for that document
    """
    # for file access convert bedrock locale to legal-docs equivalent
    if locale in BEDROCK_LOCALES_TO_LEGAL_DOCS:
        locale = BEDROCK_LOCALES_TO_LEGAL_DOCS[locale]

    source_dir = path.join(LEGAL_DOCS_PATH, doc_name)
    source_file = path.join(source_dir, locale + '.md')
    output = io.StringIO()
    locales = [f.replace('.md', '') for f in listdir(source_dir) if f.endswith('.md')]
    # convert legal-docs locales to bedrock equivalents
    locales = [LEGAL_DOCS_LOCALES_TO_BEDROCK.get(l, l) for l in locales]
    # filter out non-production locales
    locales = [l for l in locales if l in settings.PROD_LANGUAGES]

    # it's possible the legal-docs repo changed the filename to match our locale.
    # this makes it work for mapped locales even if the map becomes superfluous.
    if not path.exists(source_file) and locale in LEGAL_DOCS_LOCALES_TO_BEDROCK:
        locale = LEGAL_DOCS_LOCALES_TO_BEDROCK[locale]
        source_file = path.join(source_dir, locale + '.md')

    if not path.exists(source_file):
        source_file = path.join(LEGAL_DOCS_PATH, doc_name, 'en-US.md')

    try:
        # Parse the Markdown file
        md.markdownFromFile(
            input=source_file, output=output, extensions=[
                'markdown.extensions.attr_list',
                'markdown.extensions.headerid',
                OutlineExtension((('wrapper_cls', ''),))
            ])
        content = output.getvalue().decode('utf8')
    except IOError:
        content = None
    finally:
        output.close()

    return {
        'content': content,
        'active_locales': locales,
    }


class LegalDocView(TemplateView):
    """
    Generic view for loading a legal doc and displaying it with a template.

    Class attributes in addition to standard Django TemplateView:

    * legal_doc_name: The name of the folder in the legal_docs repo.
    * legal_doc_context_name: (default 'doc') template variable name for legal doc.

    This view automatically adds the `cache_page` decorator. The default timeout
    is 1 hour, configurable by setting the `LEGAL_DOCS_CACHE_TIMEOUT` setting to change
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
