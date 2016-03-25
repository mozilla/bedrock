# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import os
from subprocess import check_output, STDOUT

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


GIT = getattr(settings, 'GIT_BIN', 'git')


def git(*args):
    return check_output((GIT,) + args, stderr=STDOUT)


class Command(BaseCommand):
    help = 'Clones or updates l10n info from github'
    args = ''
    locales_repo = settings.LOCALES_REPO
    locales_path = settings.LOCALES_PATH
    locales_path_str = str(locales_path)

    def handle(self, *args, **options):
        if self.locales_path.is_dir():
            self.update_repo()
        else:
            self.clone_repo()

    @property
    def remote_name(self):
        return 'l10n-dev' if settings.DEV else 'l10n-prod'

    @property
    def branch_name(self):
        return '{}/master'.format(self.remote_name)

    def has_remote(self):
        return self.remote_name in git('remote')

    def add_remote(self):
        print('adding remote {}'.format(self.remote_name))
        git('remote', 'add', self.remote_name, self.locales_repo)

    def update_repo(self):
        if not self.locales_path.joinpath('.git').is_dir():
            raise CommandError('locale directory is not a git repo. delete it and try again.')
        os.chdir(self.locales_path_str)
        if not self.has_remote():
            self.add_remote()

        git('fetch', self.remote_name)
        git('checkout', '-f', self.branch_name)

    def clone_repo(self):
        git('clone', '--origin', self.remote_name, self.locales_repo, self.locales_path_str)
