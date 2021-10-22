# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import textwrap
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Convert a template to use Fluent for l10n"
    requires_system_checks = False

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(title="subcommand", dest="subcommand")
        subparsers.add_parser("help")

        recipe_parser = subparsers.add_parser("recipe", description="Create migration recipe from template")
        recipe_parser.add_argument("template", type=Path)

        ftl_parser = subparsers.add_parser("ftl", description="Create Fluent file with existing recipe")
        ftl_parser.add_argument("recipe_or_template", type=Path, help="Path to the recipe or the template from which the recipe was generated")
        ftl_parser.add_argument("locales", nargs="*", default=["en"], metavar="ab-CD", help="Locale codes to create ftl files for")

        template_parser = subparsers.add_parser("template", description="Create template_ftl.html file with existing recipe")
        template_parser.add_argument("template", type=Path)

        activation_parser = subparsers.add_parser("activation", description="Port activation data from .lang for a recipe/template")
        activation_parser.add_argument("recipe_or_template", type=Path, help="Path to the recipe or the template from which the recipe was generated")

    def handle(self, subcommand, **kwargs):
        if subcommand == "recipe":
            return self.create_recipe(**kwargs)
        if subcommand == "ftl":
            return self.create_ftl(**kwargs)
        if subcommand == "template":
            return self.create_template(**kwargs)
        if subcommand == "activation":
            return self.activation(**kwargs)
        return self.handle_help(**kwargs)

    def handle_help(self, **kwargs):
        self.stdout.write(
            textwrap.dedent(
                """\
            To migrate a template from .lang to Fluent, use the subcommands like so

            ./manage.py fluent recipe bedrock/app/templates/app/some.html

            # edit IDs in lib/fluent_migrations/app/some.py

            ./manage.py fluent template bedrock/app/templates/app/some.html
            ./manage.py fluent ftl bedrock/app/templates/app/some.html

            More documentation on https://bedrock.readthedocs.io/en/latest/fluent-conversion.html.
        """
            )
        )

    def create_recipe(self, template, **kwargs):
        from ._fluent_recipe import Recipe

        recipe = Recipe(self)
        recipe.handle(template)

    def create_template(self, template, **kwargs):
        from ._fluent_templater import Templater

        templater = Templater(self)
        templater.handle(template)

    def create_ftl(self, recipe_or_template, locales, **kwargs):
        from ._fluent_ftl import FTLCreator

        ftl_creator = FTLCreator(self)
        for locale in locales:
            ftl_creator.handle(recipe_or_template, locale)

    def activation(self, recipe_or_template, **kwargs):
        from ._fluent_activation import Activation

        activation = Activation(self)
        activation.handle(recipe_or_template)
