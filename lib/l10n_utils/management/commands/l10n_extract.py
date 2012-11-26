# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

from l10n_utils.gettext import pot_to_langfiles

def gettext_extract():
    call_command('extract', create=True)

class Command(BaseCommand):
    args = ''
    help = 'Extracts a .lang file with new translations'

    def handle(self, *args, **options):
        if args:
            langs = args
        else:
            langs = os.listdir(os.path.join(settings.ROOT, 'locale'))
            langs = filter(lambda x: x != 'templates', langs)
            langs = filter(lambda x: x[0] != '.' , langs)

        # This is basically a wrapper around the gettext extract
        # command, we might want to do some things around this in the
        # future
        gettext_extract()
        pot_to_langfiles()
