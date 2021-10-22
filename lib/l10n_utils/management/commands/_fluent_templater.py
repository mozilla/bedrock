# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from ._fluent import (
    GETTEXT_RE,
    TRANS_BLOCK_RE,
    get_migration_context,
    strip_whitespace,
    trans_to_lang,
)


class Templater:
    def __init__(self, cmd):
        self.stdout = cmd.stdout
        self.dependencies = {}

    def handle(self, template):
        self.dependencies.update(self.get_dependencies(template))
        with template.open("r") as tfp:
            template_str = tfp.read()
        template_str = GETTEXT_RE.sub(self.gettext_to_fluent, template_str)
        template_str = TRANS_BLOCK_RE.sub(self.trans_to_fluent, template_str)
        outname = template.stem + "_ftl.html"
        with template.with_name(outname).open("w") as tfp:
            tfp.write(template_str)

    def get_dependencies(self, template):
        context = get_migration_context(template)
        deps = {}
        for (fluent_file, fluent_id), lang_set in context.dependencies.items():
            for _, lang_string in lang_set:
                deps[lang_string] = fluent_id
        return deps

    def gettext_to_fluent(self, m):
        lang_id = strip_whitespace(m["string"])
        if lang_id not in self.dependencies:
            return m.group()
        args = ""
        if m["args"]:
            args = ", " + m["args"]
        return f"ftl('{self.dependencies[lang_id]}'{args})"

    def trans_to_fluent(self, m):
        lang_id = trans_to_lang(m["string"])
        if lang_id not in self.dependencies:
            return m.group()
        args = ""
        if m["args"]:
            args = ", " + m["args"]
        return f"{{{{ ftl('{self.dependencies[lang_id]}'{args}) }}}}"
