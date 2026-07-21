# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import copy
from uuid import uuid4

from django.core.management.base import BaseCommand

from bedrock.anonym.models import AnonymIndexPage


class Command(BaseCommand):
    help = "Injects analytics_id into NavigationLinkBlock items with has_button_appearance=True that are missing it (idempotent)"

    def handle(self, *args, **options):
        total = 0
        for page in AnonymIndexPage.objects.all():
            if not page.navigation:
                continue
            navigation = copy.deepcopy(list(page.navigation.raw_data))
            changed = False
            for item in navigation:
                value = item.get("value", {})
                if value.get("has_button_appearance") and not value.get("analytics_id"):
                    value["analytics_id"] = str(uuid4())
                    changed = True
            if changed:
                page.navigation = navigation
                page.save(update_fields=["navigation"])
                total += 1
        self.stdout.write(self.style.SUCCESS(f"Updated {total} page(s)."))
