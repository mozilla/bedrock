# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from django.apps import AppConfig
from django.db import connection
from django.db.models.signals import post_migrate


class CmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bedrock.cms"

    def ready(self):
        import bedrock.cms.signal_handlers  # noqa: F401
        from bedrock.cms.utils import warm_page_path_cache

        if "wagtailcore_page" in connection.introspection.table_names():
            # The route to take if the DB already exists in a viable state
            warm_page_path_cache()
        else:
            # The route to take the DB isn't ready yet (eg tests or an empty DB)
            post_migrate.connect(
                bedrock.cms.signal_handlers.trigger_cache_warming,
                sender=self,
            )
