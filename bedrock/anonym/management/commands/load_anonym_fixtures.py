# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand

from bedrock.anonym.fixtures.page_fixtures import create_all_test_pages


class Command(BaseCommand):
    help = "Load Anonym page fixtures for testing and visual verification in Wagtail admin."

    def handle(self, *args, **options):
        self.stdout.write("Creating Anonym test fixtures...")

        result = create_all_test_pages()

        self.stdout.write(self.style.SUCCESS("Created test fixtures:"))
        self.stdout.write(f"  - Placeholder image: {result['placeholder_image'].title}")
        self.stdout.write(f"  - Person snippet: {result['person']}")
        self.stdout.write(f"  - Index page: {result['index_page'].title}")
        self.stdout.write(f"  - Top and Bottom page: {result['top_and_bottom_page'].title}")
        self.stdout.write(f"  - Content Sub page: {result['content_sub_page'].title}")
        self.stdout.write(f"  - News page: {result['news_page'].title}")
        for page in result["news_item_pages"]:
            self.stdout.write(f"    - News item: {page.title}")
        self.stdout.write(f"  - Case Study page: {result['case_study_page'].title}")
        for page in result["case_study_item_pages"]:
            self.stdout.write(f"    - Case study item: {page.title}")
        self.stdout.write(f"  - Contact page: {result['contact_page'].title}")

        self.stdout.write(self.style.SUCCESS("\nAll Anonym fixtures loaded successfully! View them in Wagtail admin at /admin/pages/"))
