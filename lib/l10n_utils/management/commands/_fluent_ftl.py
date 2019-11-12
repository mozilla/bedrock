# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.conf import settings

from ._fluent import (
    get_migration_context,
)


class FTLCreator:
    def __init__(self, cmd):
        self.stdout = cmd.stdout

    def handle(self, recipe_or_template, locale):
        no_reference = locale == 'en'
        context = get_migration_context(recipe_or_template, locale=locale)
        if no_reference:
            base = settings.FLUENT_LOCAL_PATH
        else:
            base = settings.FLUENT_REPO_PATH
        for path, contents in context.serialize_changeset(None).items():
            en_path = base / locale / path
            en_path.parent.mkdir(parents=True, exist_ok=True)
            with en_path.open('w') as ftl_file:
                ftl_file.write(contents)
