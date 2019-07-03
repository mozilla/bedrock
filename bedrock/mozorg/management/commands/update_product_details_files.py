from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from product_details.storage import PDDatabaseStorage, PDFileStorage

from bedrock.utils.git import GitRepo

FIREFOX_VERSION_KEYS = (
    'FIREFOX_NIGHTLY',
    'FIREFOX_DEVEDITION',
    'FIREFOX_ESR',
    'FIREFOX_ESR_NEXT',
    'LATEST_FIREFOX_DEVEL_VERSION',
    'LATEST_FIREFOX_RELEASED_DEVEL_VERSION',
    'LATEST_FIREFOX_VERSION',
)


class Command(BaseCommand):
    def __init__(self, stdout=None, stderr=None, no_color=False):
        self.file_storage = PDFileStorage(json_dir=settings.PROD_DETAILS_TEST_DIR)
        self.db_storage = PDDatabaseStorage()
        self.repo = GitRepo(settings.PROD_DETAILS_JSON_REPO_PATH,
                            settings.PROD_DETAILS_JSON_REPO_URI,
                            name='Product Details')
        super(Command, self).__init__(stdout, stderr, no_color)

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('--database', default='default',
                            help=('Specifies the database to use, if using a db. '
                                  'Defaults to "default".')),

    def handle(self, *args, **options):
        # don't really care about deleted files. almost never happens in p-d.
        if not self.update_file_data():
            if not options['quiet']:
                print('Product Details data was already up to date')
            return

        try:
            self.validate_data()
        except Exception:
            raise CommandError('Product Details data is invalid')

        if not options['quiet']:
            print('Product Details data is valid')

        if not settings.PROD_DETAILS_STORAGE.endswith('PDDatabaseStorage'):
            # no need to continue if not using DB backend
            return

        self.load_changes(options, self.file_storage.all_json_files())
        self.repo.set_db_latest()

        if not options['quiet']:
            print('Product Details data update is complete')

    def load_changes(self, options, modified_files):
        with transaction.atomic(using=options['database']):
            for filename in modified_files:
                self.db_storage.update(filename,
                                       self.file_storage.content(filename),
                                       self.file_storage.last_modified(filename))
                if not options['quiet']:
                    print('Updated ' + filename)

            self.db_storage.update('/', '', self.file_storage.last_modified('/'))
            self.db_storage.update('regions/', '', self.file_storage.last_modified('regions/'))

    def update_file_data(self):
        self.repo.update()
        return self.repo.has_changes()

    def count_builds(self, version_key, min_builds=20):
        version = self.file_storage.data('firefox_versions.json')[version_key]
        if not version:
            if version_key == 'FIREFOX_ESR_NEXT':
                return
        builds = len([locale for locale, build in
                      self.file_storage.data('firefox_primary_builds.json').items()
                      if version in build])
        if builds < min_builds:
            raise ValueError('Too few builds for {}'.format(version_key))

    def validate_data(self):
        self.file_storage.clear_cache()
        for key in FIREFOX_VERSION_KEYS:
            self.count_builds(key)
