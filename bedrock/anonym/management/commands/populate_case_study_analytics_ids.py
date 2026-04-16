# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from uuid import uuid4

from django.core.management.base import BaseCommand

from bedrock.anonym.models import AnonymContentSubPage, AnonymIndexPage


class Command(BaseCommand):
    help = "Restructures CaseStudyListBlock items from int PKs to {page, analytics_id} structs (idempotent)"

    def handle(self, *args, **options):
        page_models = [AnonymIndexPage, AnonymContentSubPage]
        total = 0
        for Model in page_models:
            for page in Model.objects.all():
                if not page.content:
                    continue
                content = copy.deepcopy(list(page.content.raw_data))
                changed = False
                for block in content:
                    if block.get("type") != "section":
                        continue
                    for inner_block in block.get("value", {}).get("section_content", []):
                        if inner_block.get("type") != "case_study_item_list_block":
                            continue
                        for item in inner_block.get("value", {}).get("case_study_items", []):
                            item_val = item.get("value")
                            if isinstance(item_val, int):
                                # If the item is a bare PK, set a new object as the value
                                item["value"] = {"page": item_val, "analytics_id": str(uuid4())}
                                changed = True
                            elif isinstance(item_val, dict) and not item_val.get("analytics_id"):
                                # If the item has an empty analytics_id, fill it in
                                item_val["analytics_id"] = str(uuid4())
                                changed = True
                if changed:
                    page.content = content
                    page.save(update_fields=["content"])
                    total += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {total} page(s)."))
