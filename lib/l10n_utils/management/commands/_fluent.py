# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from importlib import import_module
import re

from django.conf import settings

from fluent.migrate.context import MergeContext


def migration_name(template):
    'Derive migration name from template name'
    for parent in template.parents:
        if parent.name == 'templates':
            break
    return template.relative_to(parent).with_suffix('')


def get_migration_context(template, locale='en'):
    'Create the merge context associated with the template'
    pkg_name = '.'.join(('',) + migration_name(template).parts)
    migration = import_module(pkg_name, 'l10n.bedrock_migrations')
    no_reference = locale == 'en'
    if no_reference:
        ref_dir = None
        # we're using the base localization (en-US) to create en
        locale = settings.LANGUAGE_CODE
    else:
        ref_dir = settings.FLUENT_LOCAL_PATH / 'en'
    context = MergeContext(
        locale, ref_dir, settings.LOCALES_PATH / locale
    )
    migration.migrate(context)
    return context


ADD_LANG_RE = re.compile(r'{% add_lang_files (.*?) %}')
GETTEXT_RE = re.compile(r'\b_\([\'"](?P<string>.+?)[\'"]\)'
                        r'(\s*\|\s*format\((?P<args>\w.+?)\))?', re.S)
TRANS_BLOCK_RE = re.compile(r'{%-?\s+trans\s+((?P<args>\w.+?)\s+)?-?%\}\s*'
                            r'(?P<string>.+?)'
                            r'\s*{%-?\s+endtrans\s+-?%\}', re.S)
