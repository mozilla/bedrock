import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

from l10n_utils.gettext import extract_lang_files

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

        gettext_extract()
        extract_lang_files(langs)
