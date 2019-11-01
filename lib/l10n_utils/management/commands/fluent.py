# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Convert a template to use Fluent for l10n'
    requires_system_checks = False

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(
            title='subcommand', dest='subcommand'
        )
        subparsers.add_parser('help')
        recipe_parser = subparsers.add_parser(
            'recipe',
            description='Create migration recipe from template'
        )
        recipe_parser.add_argument('template', type=Path)

    def handle(self, subcommand, **kwargs):
        if subcommand in (None, 'help'):
            return self.handle_help(**kwargs)
        if subcommand == 'recipe':
            return self.create_recipe(**kwargs)

    def handle_help(self, **kwargs):
        self.stdout.write('''\
To migrate a template from .lang to Fluent, use the subcommands like so

./manage.py fluent recipe bedrock/app/templates/app/some.html

# edit IDs in lib/fluent_migrations/app/some.py

More documentation on https://bedrock.readthedocs.io/en/latest/fluent-conversion.html.
        ''')

    def create_recipe(self, template, **kwargs):
        from ._fluent_recipe import Recipe
        recipe = Recipe(self)
        recipe.handle(template)
