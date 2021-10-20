# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

from django.test.utils import override_settings

from lib.l10n_utils.dotlang import get_translations_for_langfile

from ._fluent import get_lang_files, template_name


class Activation:
    def __init__(self, cmd):
        self.stdout = cmd.stdout
        self.dependencies = {}

    def handle(self, recipe_or_template):
        if recipe_or_template.suffix == ".py":
            template = template_name(recipe_or_template)
        else:
            template = recipe_or_template
        with template.open("r") as tfh:
            template_str = tfh.read()
        lang_files = get_lang_files(template, template_str)
        for lang_file in lang_files:
            with override_settings(DEV=False):
                locales = get_translations_for_langfile(lang_file.with_suffix(""))
            if len(locales) < 2:
                # Not the relevant lang file, probably
                continue
            print(json.dumps({"active_locales": locales}, indent=2))
