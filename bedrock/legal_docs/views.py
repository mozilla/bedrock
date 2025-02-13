# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.http import Http404
from django.views.generic import TemplateView

from bedrock.legal_docs.models import LegalDoc
from lib import l10n_utils


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
            doc = LegalDoc.objects.get_doc(doc_name, "en")
        except LegalDoc.DoesNotExist:
            try:
                doc = LegalDoc.objects.get_doc(doc_name, "en-US")
            except LegalDoc.DoesNotExist:
                doc = None

    return doc


class LegalDocView(l10n_utils.RequireSafeMixin, TemplateView):
    """
    Generic view for loading a legal doc and displaying it with a template.

    Class attributes in addition to standard Django TemplateView:

    * legal_doc_name: The name of the folder in the legal_docs repo.
    * legal_doc_context_name: (default 'doc') template variable name for legal doc.

    See `bedrock/privacy/views.py` for usage examples.
    """

    legal_doc_name = None
    legal_doc_context_name = "doc"
    ftl_files = None

    def get_legal_doc(self):
        locale = l10n_utils.get_locale(self.request)
        return load_legal_doc(self.legal_doc_name, locale)

    def render_to_response(self, context, **response_kwargs):
        response_kwargs.setdefault("content_type", self.content_type)
        _ftl_files = [
                "mozorg/about/legal",
                "privacy/index",
            ]
        if self.ftl_files:
            _ftl_files += self.ftl_files

        return l10n_utils.render(
            self.request,
            self.get_template_names()[0],
            context,
            ftl_files=_ftl_files,
            **response_kwargs,
        )

    def get_context_data(self, **kwargs):
        legal_doc = self.get_legal_doc()
        if legal_doc is None:
            raise Http404("Legal doc not found")

        context = super().get_context_data(**kwargs)
        context[self.legal_doc_context_name] = legal_doc["content"]
        context["active_locales"] = legal_doc["active_locales"]
        return context
