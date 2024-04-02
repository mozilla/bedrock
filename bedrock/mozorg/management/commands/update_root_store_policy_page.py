# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""Management command to update the root-store cert policy HTML.
NOT designed (or needed) to be run on a cron - manual use only."""

import re

from django.core.management.base import BaseCommand
from django.utils.text import slugify

import requests
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from bedrock.utils.management.decorators import alert_sentry_on_exception

SOURCE_CERT_POLICY_DOCUMENT_URL = "https://raw.githubusercontent.com/mozilla/pkipolicy/master/rootstore/policy.md"
OUTPUT_FILE_PATH = "bedrock/mozorg/templates/mozorg/about/governance/policies/security/certs/policy.html"
WRAPPING_TEMPLATE_PATH = "bedrock/mozorg/templates/mozorg/about/governance/policies/security/certs/_policy_skeleton.html"


@alert_sentry_on_exception
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            default=False,
            help="Generate the page and print it, but don't save it.",
        )
        parser.add_argument(
            "-q",
            "--quiet",
            action="store_true",
            dest="quiet",
            default=False,
            help="If no error occurs, swallow all output.",
        )
        parser.add_argument(
            "--source",
            action="store",
            dest="source_url",
            default=SOURCE_CERT_POLICY_DOCUMENT_URL,
            help=f"URL to load the policy from. Defaults to {SOURCE_CERT_POLICY_DOCUMENT_URL}",
        )
        parser.add_argument(
            "--dest",
            action="store",
            dest="dest_path",
            default=OUTPUT_FILE_PATH,
            help=f"Path to save the generated file to. Defaults to {OUTPUT_FILE_PATH}",
        )

    def output(self, msg, quiet=None):
        if not quiet and not self.quiet:
            print(msg)

    def _wrap_html_with_django_template(self, html):
        # Note: we don't want to render the actual template at this stage,
        # we just want to augment what's IN the template with the HTML from
        # the Policy doc, rendered from Markdown
        with open(WRAPPING_TEMPLATE_PATH, "r") as fp:
            template = fp.read()
        wrapped_html = template.replace("__HTML_POLICY_CONTENT_PLACEHOLDER__", html)
        return wrapped_html

    def _add_class_to_element(self, tag, klass):
        tag["class"] = klass
        return tag

    def _add_header_anchors(self, soup):
        headings = soup.find_all(re.compile("h[0-9]{1}"))
        for heading in headings:
            heading["id"] = slugify(heading.text)
        return soup

    def _add_toc(self, soup):
        h2s = soup.find_all("h2")

        toc_list = soup.new_tag("ol")
        toc_list["class"] = "mzp-u-list-styled"
        toc_list.append("\n")
        for h2 in reversed(h2s):
            new_li = soup.new_tag("li")
            new_link = soup.new_tag("a", href=f"#{h2['id']}")  # new link with anchor
            new_link.append(h2.text.partition(" ")[-1].strip())  # drop the numbering from the title
            new_li.append(new_link)
            toc_list.insert(0, "\n")
            toc_list.insert(1, "  ")  # indentation for the li that's coming
            toc_list.insert(2, new_li)

        # slide it in before the first h2
        soup.h2.insert_before("\n")
        soup.h2.insert_before(toc_list)
        soup.h2.insert_before("\n\n")
        return soup

    def _tidy_html(self, html):
        """
        1. Add the `class="mzp-c-article-title"` attribute to the `<h1>`
           (or just keep that line)
        2. Add `class="mzp-u-list-styled"` to any top-level `<ol>` or `<ul>` elements
           (no class is required on nested lists)
        3. Adds anchors to all heading elements
        4. Add the table of contents as an ordered list above the introduction,
           with links to each top-level heading.
        """

        soup = BeautifulSoup(html, "html5lib")
        h1 = soup.find("h1")
        assert h1, "No h1 found!"
        h1 = self._add_class_to_element(h1, "mzp-c-article-title")

        # We only want the top-level list elements - i.e. the direct children of <body>
        list_items = soup.find("body").find_all(["ul", "ol"], recursive=False)
        assert len(list_items) > 0, "No list items found!"
        for item in list_items:
            item = self._add_class_to_element(item, "mzp-u-list-styled")

        soup = self._add_header_anchors(soup)

        soup = self._add_toc(soup)

        # We only want the children of the body element, not any fixed up full
        # <html> node and its children.
        return "".join([str(x) for x in soup.body.children])

    def handle(self, *args, **options):
        self.quiet = options["quiet"]
        source_url = options["source_url"]
        dest_path = options["dest_path"]
        dry_run = options["dry_run"]

        self.output(f"Loading Policy doc from {source_url}")

        resp = requests.get(source_url)
        resp.raise_for_status()
        text = resp.text

        md = MarkdownIt("commonmark")
        html = md.render(text)

        self.output("Tidying up the HTML")

        tidied_html = self._tidy_html(html)

        self.output("Wrapping tidied HTML with Django template markup")

        wrapped_html = self._wrap_html_with_django_template(tidied_html)

        if dry_run:
            self.output("DRY RUN ONLY", quiet=False)
            self.output(wrapped_html, quiet=False)
        else:
            self.output(f"Writing HTML to {dest_path}")
            with open(
                dest_path,
                "w",
                encoding="utf-8",
                errors="xmlcharrefreplace",
            ) as output_file:
                output_file.write(wrapped_html)

        self.output("Done!")
