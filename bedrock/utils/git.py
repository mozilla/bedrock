# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import os
from shutil import rmtree
from subprocess import check_output, STDOUT

from django.conf import settings

from pathlib2 import Path


GIT = getattr(settings, 'GIT_BIN', 'git')


class GitRepo(object):
    def __init__(self, path, remote_url=None, remote_name=None, branch_name='master'):
        self.path = Path(path)
        self.path_str = str(self.path)
        self.remote_url = remote_url
        self.branch_name = branch_name
        if not remote_name:
            remote_name = 'bedrock-dev' if settings.DEV else 'bedrock-prod'

        self.remote_name = remote_name

    def git(self, *args):
        curdir = os.getcwd()
        try:
            os.chdir(self.path_str)
            output = check_output((GIT,) + args, stderr=STDOUT)
        finally:
            os.chdir(curdir)

        return output.strip()

    @property
    def full_branch_name(self):
        return '{}/{}'.format(self.remote_name, self.branch_name)

    @property
    def current_hash(self):
        return self.git('rev-parse', 'HEAD')

    @property
    def remote_names(self):
        return self.git('remote').split()

    def has_remote(self):
        return self.remote_name in self.remote_names

    def add_remote(self):
        if not self.remote_url:
            raise RuntimeError('remote_url required to add a remote')

        self.git('remote', 'add', self.remote_name, self.remote_url)

    def diff(self, start_hash, end_hash):
        return self.git('diff', '--name-only', start_hash, end_hash).split()

    def clone(self):
        if not self.remote_url:
            raise RuntimeError('remote_url required to clone')

        self.path.mkdir(parents=True, exist_ok=True)
        self.git('clone', '--origin', self.remote_name, '--depth', '1',
                 self.remote_url, '.')

    def pull(self):
        if not self.has_remote():
            self.add_remote()

        old_hash = self.current_hash
        self.git('fetch', self.remote_name)
        self.git('checkout', '-f', self.full_branch_name)
        return old_hash, self.current_hash

    def update(self):
        """Updates a repo, cloning if necessary.

        :return list of modified files if updated, None if cloned
        """
        if self.path.is_dir():
            if not self.path.joinpath('.git').is_dir():
                rmtree(self.path_str, ignore_errors=True)
                self.clone()
            else:
                return self.diff(*self.pull())
        else:
            self.clone()
