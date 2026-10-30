# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io
import logging
import re

from django.conf import settings
from django.db import models, transaction

import markdown as md
from mdx_outline import OutlineExtension

logger = logging.getLogger(__name__)

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
        if "\x00" in content:
            logger.warning("Could not process legal doc %s: it contains NUL characters", file_path)
            content = None
    except (OSError, UnicodeDecodeError) as exc:
        logger.warning("Could not process legal doc %s: %s", file_path, exc)
        content = None
    finally:
        output.close()

    return content


def is_legacy_layout(file_path):
    return bool(LOCALE_RE.match(file_path.stem))


def get_data_from_file_path(file_path):
    locale = file_path.parts[-2]
    doc_name = file_path.stem
    if is_legacy_layout(file_path):
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
        name_max_length = LegalDoc._meta.get_field("name").max_length
        locale_max_length = LegalDoc._meta.get_field("locale").max_length
        seen_docs = {}
        with transaction.atomic(using=self.db):
            self.all().delete()
            # read the new layout first, so a legacy copy is the one dropped
            doc_files = sorted(docs_path.glob("*/*.md"), key=lambda path: (is_legacy_layout(path), str(path)))
            for docf in doc_files:
                path_data = get_data_from_file_path(docf)
                if len(path_data["doc_name"]) > name_max_length or len(path_data["locale"]) > locale_max_length:
                    logger.warning("Legal doc %s has a name or locale too long to store", docf)
                    errors += 1
                    continue

                doc_key = (path_data["doc_name"], path_data["locale"])
                if doc_key in seen_docs:
                    logger.warning("Legal doc %s duplicates %s in the other folder layout, ignoring it", docf, seen_docs[doc_key])
                    continue

                content = process_md_file(docf)
                if content == "":
                    logger.warning("Legal doc %s is empty", docf)
                if not content:
                    errors += 1
                    # leave the name free for a usable copy in the other layout
                    continue

                seen_docs[doc_key] = docf
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
