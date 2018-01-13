# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import print_function, unicode_literals

import os
from hashlib import sha256
from shutil import rmtree
from subprocess import check_output, STDOUT
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from django.conf import settings

from pathlib2 import Path

from bedrock.utils.models import GitRepoState


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
        db_latest_key = '%s:%s:%s:%s' % (self.path_str, remote_url or '',
                                              remote_name, branch_name)
        self.db_latest_key = sha256(db_latest_key).hexdigest()

    def git(self, *args):
        """Run a git command against the current repo"""
        curdir = os.getcwd()
        try:
            os.chdir(self.path_str)
            output = check_output((GIT,) + args, stderr=STDOUT)
        finally:
            os.chdir(curdir)

        return output.strip()

    @property
    def full_branch_name(self):
        """Full branch name with remote (e.g. origin/master)"""
        return '{}/{}'.format(self.remote_name, self.branch_name)

    @property
    def current_hash(self):
        """The git revision ID (hash) of the current HEAD or None if no repo"""
        try:
            return self.git('rev-parse', 'HEAD')
        except OSError:
            return None

    @property
    def remote_names(self):
        """Return a list of the remote names in the repo or None if no repo"""
        try:
            return self.git('remote').split()
        except OSError:
            return None

    def has_remote(self):
        """Return True if the repo has a remote by the correct name"""
        return self.remote_name in self.remote_names

    def add_remote(self):
        """Add the remote to the git repo from the init args"""
        if not self.remote_url:
            raise RuntimeError('remote_url required to add a remote')

        self.git('remote', 'add', self.remote_name, self.remote_url)

    def diff(self, start_hash, end_hash):
        """Return a 2 tuple: (modified files, deleted files)"""
        diff_out = StringIO(self.git('diff', '--name-status', start_hash, end_hash))
        modified = set()
        removed = set()
        for line in diff_out:
            parts = line.split()
            # delete
            if parts[0] == 'D':
                removed.add(parts[1])
            # rename
            elif parts[0][0] == 'R':
                removed.add(parts[1])
                modified.add(parts[2])
            # everything else
            else:
                # some types (like copy) have two file entries
                for part in parts[1:]:
                    modified.add(part)

        return modified, removed

    def clone(self):
        """Clone the repo specified in the initial arguments"""
        if not self.remote_url:
            raise RuntimeError('remote_url required to clone')

        self.path.mkdir(parents=True, exist_ok=True)
        self.git('clone', '--origin', self.remote_name, '--depth', '1',
                 '--branch', self.branch_name, self.remote_url, '.')

    def pull(self):
        """Update the repo to the latest of the remote and branch

        Return the previous hash and the new hash."""
        if not self.has_remote():
            self.add_remote()

        old_hash = self.current_hash
        self.git('fetch', self.remote_name)
        self.git('checkout', '-f', self.full_branch_name)
        return old_hash, self.current_hash

    def update(self):
        """Updates a repo, cloning if necessary.

        :return a tuple of lists of modified and deleted files if updated, None if cloned
        """
        if self.path.is_dir():
            if not self.path.joinpath('.git').is_dir():
                rmtree(self.path_str, ignore_errors=True)
                self.clone()
            else:
                return self.pull()
        else:
            self.clone()

        return None, None

    def reset(self, new_head):
        self.git('reset', '--hard', new_head)

    def get_db_latest(self):
        try:
            return GitRepoState.objects.get(repo_id=self.db_latest_key).latest_ref
        except GitRepoState.DoesNotExist:
            return None

    def has_changes(self):
        return self.current_hash != self.get_db_latest()

    def set_db_latest(self, latest_ref=None):
        latest_ref = latest_ref or self.current_hash
        rs, created = GitRepoState.objects.get_or_create(repo_id=self.db_latest_key,
                                                         defaults={'latest_ref': latest_ref})
        if not created:
            rs.latest_ref = latest_ref
            rs.save()
