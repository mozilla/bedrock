# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.core.management.base import BaseCommand
from django.conf import settings

from lib.l10n_utils.gettext import merge_lang_files


class Command(BaseCommand):
    help = 'Merges gettext strings into .lang files'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('langs', nargs='*')

    def handle(self, *args, **options):
        langs = options['langs']
        if not langs:
            langs = os.listdir(os.path.join(settings.ROOT, 'locale'))
            langs = [x for x in langs if x != 'templates']
            langs = [x for x in langs if x[0] != '.']

        merge_lang_files(langs)
