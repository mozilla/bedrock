# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from importlib import import_module
import re

from django.conf import settings

from lib.l10n_utils.utils import strip_whitespace
from fluent.migrate.context import MigrationContext


def migration_name(template):
    'Derive migration name from template name'
    for parent in template.parents:
        if parent.name == 'templates':
            break
    return template.relative_to(parent).with_suffix('')


def get_migration_context(recipe_or_template, locale='en'):
    'Create the merge context associated with the template or recipe'
    if recipe_or_template.suffix == '.py':
        name = recipe_or_template.resolve().relative_to(settings.FLUENT_MIGRATIONS_PATH).with_suffix('')
    else:
        name = migration_name(recipe_or_template)
    pkg_name = '.'.join(('',) + name.parts)
    migration = import_module(pkg_name, settings.FLUENT_MIGRATIONS)
    no_reference = locale == 'en'
    if no_reference:
        ref_dir = None
        # we're using the base localization (en-US) to create en
        locale = settings.LANGUAGE_CODE
    else:
        ref_dir = settings.FLUENT_LOCAL_PATH / 'en'
    context = MigrationContext(
        locale, ref_dir, settings.LOCALES_PATH / locale
    )
    migration.migrate(context)
    return context


def trans_to_lang(string):
    string = strip_whitespace(string)
    return TRANS_PLACEABLE_RE.sub(
        lambda m: '%({})s'.format(m.group('var')),
        string
    )


ADD_LANG_RE = re.compile(r'{% (?:add|set)_lang_files (.*?) %}')
GETTEXT_RE = re.compile(r'\b_\([\'"](?P<string>.+?)[\'"]\)'
                        r'(\s*\|\s*format\((?P<args>\w.+?)\))?', re.S)
TRANS_BLOCK_RE = re.compile(r'{%-?\s+trans\s+((?P<args>\w.+?)\s+)?-?%\}\s*'
                            r'(?P<string>.+?)'
                            r'\s*{%-?\s+endtrans\s+-?%\}', re.S)
TRANS_PLACEABLE_RE = re.compile(r'{{\s*(?P<var>\w+)\s*}}')
