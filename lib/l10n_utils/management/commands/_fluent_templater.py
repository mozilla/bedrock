# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from importlib import import_module

from django.conf import settings

from fluent.migrate.context import MergeContext

from ._fluent import (
    migration_name,
    GETTEXT_RE,
)


class Templater:
    def __init__(self, cmd):
        self.stdout = cmd.stdout
        self.dependencies = {}

    def handle(self, template):
        self.dependencies.update(self.get_dependencies(template))
        with template.open('r') as tfp:
            template_str = tfp.read()
        template_str = GETTEXT_RE.sub(self.to_fluent, template_str)
        outname = template.stem + '_ftl.html'
        with template.with_name(outname).open('w') as tfp:
            tfp.write(template_str)

    def get_dependencies(self, template):
        pkg_name = '.'.join(('',) + migration_name(template).parts)
        migration = import_module(pkg_name, 'l10n.bedrock_migrations')
        context = MergeContext(
            settings.LANGUAGE_CODE, None, settings.LOCALES_PATH / settings.LANGUAGE_CODE
        )
        migration.migrate(context)
        deps = {}
        for (fluent_file, fluent_id), lang_set in context.dependencies.items():
            for _, lang_string in lang_set:
                deps[lang_string] = fluent_id
        return deps

    def to_fluent(self, m):
        if not m.group('string') in self.dependencies:
            return m.group()
        return f"ftl('{self.dependencies[m.group('string')]}')"
