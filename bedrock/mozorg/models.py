# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import io

from django.conf import settings
from django.db import models, transaction

import markdown as md
from markdown.extensions.toc import TocExtension


def process_md_file(file_path):
    output = io.BytesIO()
    try:
        # Parse the Markdown file
        md.markdownFromFile(
            input=str(file_path),
            output=output,
            output_format="html5",
            extensions=[TocExtension(permalink=True)],
        )
        content = output.getvalue().decode("utf-8")
    except OSError:
        content = ""
    finally:
        output.close()

    return content


class WebvisionDocsManager(models.Manager):
    def refresh(self):
        doc_objs = []
        errors = 0
        docs_path = settings.WEBVISION_DOCS_PATH
        with transaction.atomic(using=self.db):
            self.all().delete()
            doc_files = docs_path.glob("input/*.md")
            for f in doc_files:
                name = f.stem
                content = process_md_file(f)
                if not content:
                    errors += 1
                    continue

                doc_objs.append(
                    WebvisionDoc(
                        name=name,
                        content=content,
                    )
                )
            self.bulk_create(doc_objs)

        return len(doc_objs), errors


class WebvisionDoc(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()

    objects = WebvisionDocsManager()

    def __str__(self):
        return self.name
