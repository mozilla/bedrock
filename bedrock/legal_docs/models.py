import io

from django.conf import settings
from django.db import models, transaction

import markdown as md
from mdx_outline import OutlineExtension


LEGAL_DOCS_LOCALES_TO_BEDROCK = {
    'hi': 'hi-IN',
}


def process_md_file(file_path):
    output = io.BytesIO()
    try:
        # Parse the Markdown file
        md.markdownFromFile(
            input=str(file_path), output=output, extensions=[
                'markdown.extensions.attr_list',
                'markdown.extensions.toc',
                OutlineExtension((('wrapper_cls', ''),))
            ])
        content = output.getvalue().decode('utf-8')
    except IOError:
        content = None
    finally:
        output.close()

    return content


def get_data_from_file_path(file_path):
    locale = file_path.stem
    if locale in LEGAL_DOCS_LOCALES_TO_BEDROCK:
        locale = LEGAL_DOCS_LOCALES_TO_BEDROCK[locale]
    doc_name = file_path.parts[-2]
    return {
        'locale': locale,
        'doc_name': doc_name,
    }


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
        doc = self.get(name=doc_name, locale=locale)
        all_locales = self.filter(name=doc_name).values_list('locale', flat=True)
        return {
            'content': doc.content,
            'active_locales': sorted(all_locales),
        }

    def refresh(self):
        doc_objs = []
        errors = 0
        docs_path = settings.LEGAL_DOCS_PATH
        with transaction.atomic(using=self.db):
            self.all().delete()
            doc_files = docs_path.glob('*/*.md')
            for docf in doc_files:
                path_data = get_data_from_file_path(docf)
                content = process_md_file(docf)
                if not content:
                    errors += 1
                    continue

                doc_objs.append(LegalDoc(
                    name=path_data['doc_name'],
                    locale=path_data['locale'],
                    content=content,
                ))
            self.bulk_create(doc_objs)

        return len(doc_objs), errors


class LegalDoc(models.Model):
    name = models.CharField(max_length=100)
    locale = models.CharField(max_length=5)
    content = models.TextField()

    objects = LegalDocsManager()

    def __str__(self):
        return f'{self.name} - {self.locale}'
