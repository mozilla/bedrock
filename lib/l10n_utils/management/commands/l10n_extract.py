import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

from l10n_utils.gettext import extract_lang

def gettext_extract():
    call_command('extract', create=True)

class Command(BaseCommand):
    args = ''
    help = 'Extracts a .lang file with new translations'

    def handle(self, *args, **options):
        if args:
            output_file = args
        else:
            output_file = os.path.join(settings.ROOT,
                                       'locale/templates/new.lang')

        gettext_extract()
        extract_lang(output_file)



