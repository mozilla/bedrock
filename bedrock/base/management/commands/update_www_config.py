from __future__ import print_function

import os

from django.conf import settings
from django.core.management.base import BaseCommand

from envcat import get_unique_vars

from bedrock.base.models import ConfigValue
from bedrock.utils.git import GitRepo


def get_config_file_names(*args):
    return [os.path.join(settings.WWW_CONFIG_PATH, 'configs', '%s.env' % fn)
            for fn in args]


def get_config_values():
    app_name = settings.DEIS_APP or 'bedrock-dev'
    return get_unique_vars(get_config_file_names('global', app_name))


def refresh_db_values():
    ConfigValue.objects.all().delete()
    values = get_config_values()
    count = 0
    for name, value in values.iteritems():
        if value:
            ConfigValue.objects.create(name=name, value=value)
            count += 1

    return count


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-q', '--quiet', action='store_true', dest='quiet', default=False,
                            help='If no error occurs, swallow all output.'),
        parser.add_argument('-f', '--force', action='store_true', dest='force', default=False,
                            help='Load the data even if nothing new from git.'),

    def output(self, msg):
        if not self.quiet:
            print(msg)

    def handle(self, *args, **options):
        self.quiet = options['quiet']
        repo = GitRepo(settings.WWW_CONFIG_PATH, settings.WWW_CONFIG_REPO,
                       branch_name=settings.WWW_CONFIG_BRANCH)
        self.output('Updating git repo')
        repo.update()
        if not (options['force'] or repo.has_changes()):
            self.output('No config updates')
            return

        self.output('Loading configs into database')
        count = refresh_db_values()

        self.output('%s configs successfully loaded' % count)

        repo.set_db_latest()

        self.output('Saved latest git repo state to database')
        self.output('Done!')
