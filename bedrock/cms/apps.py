# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bedrock.cms"

    def ready(self):
        from wagtail import hooks

        # Find and remove the existing hook function that creates page aliases on synctree.

        # `hooks.get_hooks()`` does a broader search for hooks and updates/fully populates `hooks._hooks``
        after_create_page_hooks = hooks.get_hooks("after_create_page")

        for hook in after_create_page_hooks:
            if hook.__module__ == "wagtail_localize.synctree" and hook.__name__ == "after_create_page":
                logger.info("Patching to remove the 'after_create_page' hook from 'wagtail_localize.synctree'")

                # hookspec below is a tuple of (hook_func, position_int)
                reduced_hooks = [hookspec for hookspec in hooks._hooks["after_create_page"] if hookspec[0] != hook]

                # Warning: internal attribute, may break in the future (so we have a test that checks this works)
                hooks._hooks["after_create_page"] = reduced_hooks
