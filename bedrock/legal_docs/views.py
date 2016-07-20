# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from os import path, listdir
import StringIO

from django.conf import settings
from django.http import Http404
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView

import markdown as md
from mdx_outline import OutlineExtension

from bedrock.settings import path as base_path
from lib import l10n_utils
from product_details import product_details

LEGAL_DOCS_PATH = base_path('vendor-local', 'src', 'legal-docs')
CACHE_TIMEOUT = getattr(settings, 'LEGAL_DOCS_CACHE_TIMEOUT', 60 * 60)


def load_legal_doc(doc_name, locale):
    """
    Return the HTML content of a legal doc in the requested locale.

    :param doc_name: name of the legal doc folder
    :param locale: preferred language version of the doc
    :return: dict containing string content of the file (or None), a boolean
             value indicating whether the file is localized into the specified
             locale, and a dict of all available locales for that document
    """
    source_dir = path.join(LEGAL_DOCS_PATH, doc_name)
    source_file = path.join(source_dir, locale + '.md')
    output = StringIO.StringIO()
    locales = [f.replace('.md', '') for f in listdir(source_dir) if f.endswith('.md')]
    localized = locale != settings.LANGUAGE_CODE
    translations = {}

    if not path.exists(source_file):
        source_file = path.join(LEGAL_DOCS_PATH, doc_name, 'en-US.md')
        localized = False

    try:
        # Parse the Markdown file
        md.markdownFromFile(input=source_file, output=output,
                            extensions=['attr_list', 'headerid',
                                        OutlineExtension((('wrapper_cls', None),))])
        content = output.getvalue().decode('utf8')
    except IOError:
        content = None
        localized = False
    finally:
        output.close()

    for lang in locales:
        if lang in product_details.languages:
            translations[lang] = product_details.languages[lang]['native']

    return {
        'content': content,
        'localized': localized,
        'translations': translations,
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
        context['localized'] = legal_doc['localized']
        context['translations'] = legal_doc['translations']
        return context

    @classmethod
    def as_view(cls, **initkwargs):
        cache_timeout = initkwargs.pop('cache_timeout', cls.cache_timeout)
        return cache_page(cache_timeout)(super(LegalDocView, cls).as_view(**initkwargs))
