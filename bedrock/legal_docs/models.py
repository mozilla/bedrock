# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import re

from django.conf import settings
from django.db import models, transaction

import markdown as md
from mdx_outline import OutlineExtension

LEGAL_DOCS_LOCALES_TO_BEDROCK = {
    "hi": "hi-IN",
}
LOCALE_RE = re.compile(r"[a-z]{2,3}(-[A-Z]{2}(_[a-z])?)?$")


def process_md_file(file_path):
    output = io.BytesIO()
    try:
        # Parse the Markdown file
        md.markdownFromFile(
            input=str(file_path),
            output=output,
            extensions=[
                "markdown.extensions.attr_list",
                "markdown.extensions.toc",
                "markdown.extensions.tables",
                OutlineExtension((("wrapper_cls", ""),)),
            ],
        )
        content = output.getvalue().decode("utf-8")
    except OSError:
        content = None
    finally:
        output.close()

    return content


def get_data_from_file_path(file_path):
    locale = file_path.parts[-2]
    doc_name = file_path.stem
    if LOCALE_RE.match(doc_name):
        # we're dealing with the old repo format
        locale, doc_name = doc_name, locale

    if locale in LEGAL_DOCS_LOCALES_TO_BEDROCK:
        locale = LEGAL_DOCS_LOCALES_TO_BEDROCK[locale]
    return {
        "locale": locale,
        "doc_name": doc_name,
    }


def snake_case(name):
    return name.lower().replace("-", "_")


class LegalDocsManager(models.Manager):
    def get_doc(self, doc_name, locale):
        """
        Return the HTML content of a legal doc in the requested locale.

        :param doc_name: name of the legal doc folder
        :param locale: preferred language version of the doc
        :return: dict containing string content of the file (or None), a boolean
                 value indicating whether the file is localized into the specified
                 locale, and a dict of all available locales for that document
        """
        try:
            doc = self.get(name=doc_name, locale=locale)
        except LegalDoc.DoesNotExist:
            # the new repo layout uses snake case
            # this allows us to transition more easily
            # TODO remove the above try and fix the doc names in the code after transition
            doc_name = snake_case(doc_name)
            doc = self.get(name=doc_name, locale=locale)

        all_locales = list(self.filter(name=doc_name).values_list("locale", flat=True))
        if "en" in all_locales:
            # legal-docs now uses "en" but the Mozorg site needs en-US.
            all_locales[all_locales.index("en")] = "en-US"

        # filter locales not active on the site
        all_locales = [loc for loc in all_locales if loc in settings.PROD_LANGUAGES]

        return {
            "content": doc.content,
            # sort and make unique
            "active_locales": sorted(set(all_locales)),
        }

    def refresh(self):
        doc_objs = []
        errors = 0
        docs_path = settings.LEGAL_DOCS_PATH
        with transaction.atomic(using=self.db):
            self.all().delete()
            doc_files = docs_path.glob("*/*.md")
            for docf in doc_files:
                path_data = get_data_from_file_path(docf)
                content = process_md_file(docf)
                if not content:
                    errors += 1
                    continue

                doc_objs.append(
                    LegalDoc(
                        name=path_data["doc_name"],
                        locale=path_data["locale"],
                        content=content,
                    )
                )
            self.bulk_create(doc_objs)

        return len(doc_objs), errors


class LegalDoc(models.Model):
    name = models.CharField(max_length=100)
    locale = models.CharField(max_length=5)
    content = models.TextField()

    objects = LegalDocsManager()

    def __str__(self):
        return f"{self.name} - {self.locale}"
