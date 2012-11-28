# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.core.management.base import BaseCommand
from django.conf import settings

from l10n_utils.gettext import merge_lang_files

class Command(BaseCommand):
    args = ''
    help = 'Merges gettext strings into .lang files'

    def handle(self, *args, **options):
        if args:
            langs = args
        else:
            langs = os.listdir(os.path.join(settings.ROOT, 'locale'))
            langs = filter(lambda x: x != 'templates', langs)
            langs = filter(lambda x: x[0] != '.' , langs)

        merge_lang_files(langs)
