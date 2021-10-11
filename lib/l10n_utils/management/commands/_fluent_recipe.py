# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
from collections import defaultdict

from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import slugify

from fluent.runtime import FluentBundle, FluentResource

from lib.l10n_utils.utils import strip_whitespace

from ._fluent import (
    GETTEXT_RE,
    TRANS_BLOCK_RE,
    get_lang_files,
    migration_name,
    trans_to_lang,
)

STR_VARIABLE_RE = re.compile(r"%(?P<var>\(\w+\))?s")
RECIPE_INTRO = """\
from __future__ import absolute_import
import fluent.syntax.ast as FTL
from fluent.migrate.helpers import transforms_from
from fluent.migrate.helpers import VARIABLE_REFERENCE, TERM_REFERENCE
from fluent.migrate import REPLACE, COPY

"""

RECIPE_SIGNATURE = '''\

def migrate(ctx):
    """Migrate {}, part {{index}}."""

'''

ADD_TRANSFORMS = """\
    ctx.add_transforms(
        "{ftl_file}",
        "{ftl_file}",
        {transforms}
        )
"""

SIMPLE_WRAPPER = '''\
transforms_from("""
{copies}
""", {from_path}={from_path})\
'''

REPLACE_TEMPLATE = """\
            FTL.Message(
                id=FTL.Identifier("{fluent_id}"),
                value=REPLACE(
                    {from_path},
                    "{lang_string}",
                    {{
{replacements}
                    }}
                )
            ),
"""

VAR_REPLACE = """\
                        "{lit}": VARIABLE_REFERENCE("{var}"),\
"""

TERM_REPLACE = """\
                        "{lit}": TERM_REFERENCE("{var}"),\
"""
BRAND_TERMS = None


def get_brand_terms():
    """Return a dict of term IDs and english strings ordered with strings longest to shortest"""
    global BRAND_TERMS
    if BRAND_TERMS is None:
        bundle = FluentBundle(["en"])
        brands_path = settings.FLUENT_LOCAL_PATH / "en" / "brands.ftl"
        with brands_path.open(encoding="utf-8") as brands_file:
            resource = FluentResource(brands_file.read())

        bundle.add_resource(resource)
        tmp_dict = {k: bundle._lookup(k, term=True).value.value for k, v in bundle._terms.items()}
        BRAND_TERMS = {k: tmp_dict[k] for k in sorted(tmp_dict, key=lambda k: len(tmp_dict[k]), reverse=True)}

    return BRAND_TERMS


def brand_terms_in_string(lang_string):
    terms = []
    for term_id, value in get_brand_terms().items():
        if value in lang_string:
            terms.append(term_id)
            lang_string = lang_string.replace(value, "")

    return terms


class Recipe:
    def __init__(self, cmd):
        self.stdout = cmd.stdout

    def handle(self, template):
        with template.open("r") as tfp:
            template_str = tfp.read()
        lang_files = get_lang_files(template, template_str)
        lang_ids = self.get_lang_ids(template_str)
        ids_for_file = self.get_ids_for_file(lang_ids, lang_files)
        recipe = RECIPE_INTRO
        for legacy, variable in lang_files.items():
            recipe += f'{variable} = "{legacy}"\n'
        recipe += RECIPE_SIGNATURE.format(template)

        for from_path, ids in ids_for_file.items():
            transforms = self.get_transforms(template.stem, ids, lang_files[from_path])
            recipe += ADD_TRANSFORMS.format(ftl_file=from_path.with_suffix(".ftl"), transforms=transforms)
        self.write_recipe_for(template, recipe)

    def get_lang_ids(self, template_str):
        found = []
        found.extend((m.start(), strip_whitespace(m["string"]), m["args"]) for m in GETTEXT_RE.finditer(template_str))
        found.extend((m.start(), trans_to_lang(m["string"]), m["args"]) for m in TRANS_BLOCK_RE.finditer(template_str))
        found.sort(key=lambda t: t[0])
        return {string: args for pos, string, args in found}

    def get_ids_for_file(self, lang_ids, lang_files):
        from compare_locales.parser import getParser

        parser = getParser("foo.lang")
        ids_for_file = defaultdict(list)
        for lf in lang_files.keys():
            f = settings.LOCALES_PATH / "en-US" / lf
            if not f.exists():
                continue
            parser.readFile(str(f))
            mapping = parser.parse()
            for string_id in lang_ids.keys():
                if string_id in mapping:
                    ids_for_file[lf].append(string_id)
        return ids_for_file

    def get_transforms(self, id_stem, lang_ids, from_path):
        transforms = ""
        simple_transforms = []
        replaces = []
        for lang_string in lang_ids:
            fluent_id = self.string_to_ftl_id(id_stem, lang_string)
            brands_in_string = brand_terms_in_string(lang_string)
            if STR_VARIABLE_RE.search(lang_string) or brands_in_string:
                if simple_transforms:
                    if transforms:
                        transforms += " + "
                    transforms += SIMPLE_WRAPPER.format(copies="\n".join(simple_transforms), from_path=from_path)
                    simple_transforms = []
                replaces.append(self.create_replace(from_path, fluent_id, lang_string, brands_in_string))
            else:
                if replaces:
                    if transforms:
                        transforms += " + "
                    transforms += "[\n"
                    transforms += "".join(replaces)
                    transforms += "        ]"
                    replaces = []
                escaped_lang_string = lang_string.replace('"', r"\"")
                simple_transforms.append(f'{fluent_id} = {"{"}COPY({from_path}, "{escaped_lang_string}",){"}"}')
        if simple_transforms:
            if transforms:
                transforms += " + "
            transforms += SIMPLE_WRAPPER.format(copies="\n".join(simple_transforms), from_path=from_path)
        if replaces:
            if transforms:
                transforms += " + "
            transforms += "[\n"
            transforms += "".join(replaces)
            transforms += "        ]"
        return transforms

    def string_to_ftl_id(self, id_stem, string):
        string = strip_tags(string)
        slug_parts = slugify(string).split("-")
        slug = id_stem
        for part in slug_parts:
            slug = "-".join([slug, part])
            if len(slug) > 30:
                break

        return slug

    def create_replace(self, from_path, fluent_id, lang_string, brands_in_string):
        replacers = {}
        replacements = ""
        for m in STR_VARIABLE_RE.finditer(lang_string):
            varname = m.group("var")
            if varname is None:
                varname = "missing-var"
            else:
                varname = varname[1:-1]
            if varname not in replacers:
                replacers[varname] = m.group()

        if replacers:
            replacements += '                        "%%": "%",\n'
            replacements += "\n".join(VAR_REPLACE.format(lit=lit, var=var) for var, lit in replacers.items())

        if brands_in_string:
            brands = get_brand_terms()
            if replacements:
                replacements += "\n"
            replacements += "\n".join(TERM_REPLACE.format(lit=brands[brand], var=brand) for brand in brands_in_string)

        return REPLACE_TEMPLATE.format(
            fluent_id=fluent_id, from_path=from_path, lang_string=lang_string.replace('"', r"\""), replacements=replacements
        )

    def write_recipe_for(self, template, recipe):
        relpath = migration_name(template).with_suffix(".py")
        mod = relpath.parent
        (settings.FLUENT_MIGRATIONS_PATH / mod).mkdir(parents=True, exist_ok=True)
        for mod in relpath.parents:
            init = settings.FLUENT_MIGRATIONS_PATH / mod / "__init__.py"
            if init.is_file():
                break
            with init.open("w") as ifd:
                ifd.write("")
        with (settings.FLUENT_MIGRATIONS_PATH / relpath).open("w") as rfd:
            rfd.write(recipe)
