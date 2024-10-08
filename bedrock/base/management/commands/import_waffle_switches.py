# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.core.management.base import BaseCommand

from waffle.models import Switch

from bedrock.base.models import ConfigValue
from bedrock.utils.management.decorators import alert_sentry_on_exception


@alert_sentry_on_exception
class Command(BaseCommand):
    def handle(self, *args, **options):
        prefix = "SWITCH_"

        for config in ConfigValue.objects.all():
            # Ignore funnelcakes and other yummy things.
            if not config.name.startswith(prefix):
                continue

            # Remove prefix.
            name = config.name[len(prefix) :]
            # Set active to boolean.
            active = config.value == "on"

            switch, created = Switch.objects.update_or_create(name=name, defaults={"active": active})
            print(f"{'Created new' if created else 'Updated'} switch: {name} = {'on' if active else 'off'}")
