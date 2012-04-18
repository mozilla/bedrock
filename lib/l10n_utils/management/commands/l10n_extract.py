import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

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

        # This is basically a wrapper around the gettext extract
        # command, we might want to do some things around this in the
        # future
        gettext_extract()

