# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from ._fluent import (
    get_lang_files,
    template_name,
)
from lib.l10n_utils.dotlang import get_translations_for_langfile


class Activation:
    def __init__(self, cmd):
        self.stdout = cmd.stdout
        self.dependencies = {}

    def handle(self, recipe_or_template):
        if recipe_or_template.suffix == '.py':
            template = template_name(recipe_or_template)
        else:
            template = recipe_or_template
        with template.open('r') as tfh:
            template_str = tfh.read()
        lang_files = get_lang_files(template, template_str)
        for lang_file in lang_files:
            locales = get_translations_for_langfile(lang_file)
            # XXX TODO
            # Where do we go from here
            print(locales)
