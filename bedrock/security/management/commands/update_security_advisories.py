# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import errno
import glob
import os
import re
import sys
from optparse import make_option
from subprocess import check_call, Popen, PIPE, STDOUT

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import NoArgsCommand, BaseCommand

from dateutil.parser import parse as parsedate

from bedrock.security.models import Product, SecurityAdvisory
from bedrock.security.utils import FILENAME_RE, chdir, parse_md_file


ADVISORIES_REPO = settings.MOFO_SECURITY_ADVISORIES_REPO
ADVISORIES_PATH = settings.MOFO_SECURITY_ADVISORIES_PATH

GIT = getattr(settings, 'GIT_BIN', 'git')
GIT_CLONE = (GIT, 'clone', ADVISORIES_REPO, ADVISORIES_PATH)
GIT_PULL = (GIT, 'pull', '--ff-only', 'origin', 'master')
GIT_GET_HASH = (GIT, 'rev-parse', 'HEAD')

SM_RE = re.compile('seamonkey', flags=re.IGNORECASE)
FNULL = open(os.devnull, 'w')


def fix_product_name(name):
    if 'seamonkey' in name.lower():
        name = SM_RE.sub('SeaMonkey', name, 1)

    if name.endswith('.0'):
        name = name[:-2]

    return name


def mkdir_p(path):
    """Mimic mkdir -p from *nix."""
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def filter_advisory_filenames(filenames):
    return [os.path.join(ADVISORIES_PATH, fn) for fn in filenames
            if FILENAME_RE.search(fn)]


@chdir(ADVISORIES_PATH)
def git_pull():
    old_hash = get_current_git_hash()
    check_call(GIT_PULL, stdout=FNULL, stderr=STDOUT)
    new_hash = get_current_git_hash()
    return old_hash, new_hash


@chdir(ADVISORIES_PATH)
def git_diff(old_hash, new_hash):
    if old_hash != new_hash:
        proc = Popen((GIT, 'diff', '--name-only', old_hash, new_hash), stdout=PIPE)
        git_out = proc.communicate()[0].split()
        return filter_advisory_filenames(git_out)

    return []


@chdir(ADVISORIES_PATH)
def update_repo():
    modified_files = []
    deleted_files = []
    mod_files = git_diff(*git_pull())
    for mf in mod_files:
        if os.path.exists(mf):
            modified_files.append(mf)
        else:
            deleted_files.append(mf)

    return modified_files, deleted_files


@chdir(ADVISORIES_PATH)
def get_current_git_hash():
    p = Popen(GIT_GET_HASH, stdout=PIPE)
    return p.communicate()[0].strip()


def delete_files(filenames):
    ids = []
    for filename in filenames:
        match = re.search('(\d{4}-\d{2,3})\.md$', filename)
        ids.append(match.group(1))

    SecurityAdvisory.objects.filter(id__in=ids).delete()


def add_or_update_advisory(data, html):
    """
    Add or update an advisory in the database.

    :param data: dict of metadata about the advisory
    :param html: HTML content of the advisory
    :return: SecurityAdvisory
    """
    mfsa_id = data.pop('mfsa_id')
    year, order = [int(x) for x in mfsa_id.split('-')]
    kwargs = {
        'id': mfsa_id,
        'title': data.pop('title'),
        'impact': data.pop('impact'),
        'reporter': data.pop('reporter', None),
        'year': year,
        'order': order,
        'html': html,
    }
    datestr = data.pop('announced', None)
    if datestr:
        dateobj = parsedate(datestr).date()
        kwargs['announced'] = dateobj
    prodver_objs = []
    for productname in data.pop('fixed_in'):
        productname = fix_product_name(productname)
        productobj, created = Product.objects.get_or_create(name=productname)
        prodver_objs.append(productobj)

    # discard products. we rely on fixed_in.
    data.pop('products', None)

    if data:
        kwargs['extra_data'] = data

    advisory = SecurityAdvisory(**kwargs)
    advisory.save()
    advisory.fixed_in.clear()
    advisory.fixed_in.add(*prodver_objs)
    return advisory


def update_db_from_file(filename):
    """
    Parse file for YAML and Markdown and update database.

    :raises: KeyError or ValueError
    :param filename: path to markdown file.
    :return: SecurityAdvisory instance
    """
    return add_or_update_advisory(*parse_md_file(filename))


def clone_repo():
    mkdir_p(ADVISORIES_PATH)
    check_call(GIT_CLONE, stdout=FNULL, stderr=STDOUT)


def get_all_md_files():
    return glob.glob(os.path.join(ADVISORIES_PATH, 'announce', '*', '*.md'))


class Command(NoArgsCommand):
    help = 'Refresh database of MoFo Security Advisories.'
    lock_key = 'command-lock:update_security_advisories'
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
        make_option('--skip-git',
                    action='store_true',
                    dest='no_git',
                    default=False,
                    help='No update, just import files (implies --force)'),
        make_option('--clear-db',
                    action='store_true',
                    dest='clear_db',
                    default=False,
                    help='Clear all security advisory data before update (implies --force)'),
    )

    def get_lock(self):
        lock = cache.get(self.lock_key)
        if not lock:
            cache.set(self.lock_key, True, 60)
            return True

        return False

    def release_lock(self):
        cache.delete(self.lock_key)

    def handle(self, *args, **options):
        if self.get_lock():
            super(Command, self).handle(*args, **options)
            self.release_lock()

    def handle_noargs(self, **options):
        quiet = options['quiet']
        force = options['force']
        no_git = options['no_git']
        clear_db = options['clear_db']
        if no_git or clear_db:
            force = True
        cloned = False

        def printout(msg, ending=None):
            if not quiet:
                self.stdout.write(msg, ending=ending)

        if clear_db:
            printout('Clearing all security advisories.')
            SecurityAdvisory.objects.all().delete()
            Product.objects.all().delete()

        if not no_git:
            if not os.path.exists(ADVISORIES_PATH):
                printout('Cloning repository.')
                clone_repo()
                cloned = True
            elif force:
                printout('Updating repository.')
                git_pull()

        if force or cloned:
            printout('Reading all files.')
            modified_files = get_all_md_files()
            deleted_files = []
        else:
            printout('Updating repository and finding modified files.')
            modified_files, deleted_files = update_repo()

        errors = []
        updates = 0
        if modified_files:
            for mf in modified_files:
                try:
                    update_db_from_file(mf)
                except Exception as e:
                    errors.append('ERROR parsing %s: %s' % (mf, e))
                    if not quiet:
                        sys.stdout.write('E')
                        sys.stdout.flush()
                    continue
                if not quiet:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                updates += 1
            printout('\nUpdated {0} files.'.format(updates))

        if deleted_files:
            delete_files(deleted_files)
            printout('Deleted {0} files.'.format(len(deleted_files)))

        if not modified_files and not deleted_files:
            printout('Nothing to update.')

        if errors:
            sys.stderr.write('Encountered {0} errors:\n\n'.format(len(errors)) +
                             '\n==========\n'.join(errors))
