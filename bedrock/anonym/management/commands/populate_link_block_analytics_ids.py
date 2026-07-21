# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from uuid import uuid4

from django.core.management.base import BaseCommand

from bedrock.anonym.models import (
    AnonymCaseStudyItemPage,
    AnonymContentSubPage,
    AnonymIndexPage,
    AnonymNewsItemPage,
)


class Command(BaseCommand):
    help = "Injects settings.analytics_id into LinkWithTextBlock instances that are missing it (idempotent)"

    def handle(self, *args, **options):
        page_models = [
            AnonymIndexPage,
            AnonymContentSubPage,
            AnonymNewsItemPage,
            AnonymCaseStudyItemPage,
        ]
        total = 0
        for Model in page_models:
            for page in Model.objects.all():
                if not page.content:
                    continue
                content = copy.deepcopy(list(page.content.raw_data))
                changed = False
                for block in content:
                    block_type = block.get("type")
                    value = block.get("value", {})
                    if block_type == "section":
                        for link_item in value.get("action", []):
                            link_val = link_item.get("value", link_item)
                            settings = link_val.setdefault("settings", {})
                            if not settings.get("analytics_id"):
                                settings["analytics_id"] = str(uuid4())
                                changed = True
                    elif block_type == "call_to_action":
                        for link_item in value.get("button", []):
                            link_val = link_item.get("value", link_item)
                            settings = link_val.setdefault("settings", {})
                            if not settings.get("analytics_id"):
                                settings["analytics_id"] = str(uuid4())
                                changed = True
                if changed:
                    page.content = content
                    page.save(update_fields=["content"])
                    total += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {total} page(s)."))
