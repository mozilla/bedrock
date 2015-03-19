from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils.module_loading import import_by_path


DEFAULT_CLASS = 'bedrock.externalfiles.ExternalFile'


class Command(BaseCommand):
    args = '[<file_id ...>]'
    help = 'Update data files from the web. Specify file IDs or none to update all.'
    option_list = BaseCommand.option_list + (
        make_option('--force',
                    action='store_true',
                    dest='force',
                    default=False,
                    help='Force updating files even if up-to-date.'),
        make_option('--quiet',
                    action='store_true',
                    dest='quiet',
                    default=False,
                    help='Do not print output to stdout.'),
        make_option('--status',
                    action='store_true',
                    dest='status',
                    default=False,
                    help='Print only a final status to stdout. Mostly for scripts.')
    )

    def handle(self, *args, **options):
        file_ids = args or settings.EXTERNAL_FILES.keys()
        updated = False

        def printout(msg, ending=None):
            if not (options['quiet'] or options['status']):
                self.stdout.write(msg, ending=ending)

        for fid in file_ids:
            try:
                finfo = settings.EXTERNAL_FILES[fid]
            except KeyError:
                raise CommandError('No external file configuration for ' + fid)
            klass = import_by_path(finfo.get('type', DEFAULT_CLASS))
            printout('updating {0}... '.format(fid), ending='')
            result = klass(fid).update(options['force'])
            if result is None:
                printout('already up-to-date')
            else:
                updated = True
                printout('done')

        if options['status']:
            if updated:
                self.stdout.write('updated')
            else:
                self.stdout.write('up-to-date')
