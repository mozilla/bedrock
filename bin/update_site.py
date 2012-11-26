#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Usage: update_site.py [options]
Updates a server's sources, vendor libraries, packages CSS/JS
assets, migrates the database, and other nifty deployment tasks.

Options:
  -h, --help            show this help message and exit
  -e ENVIRONMENT, --environment=ENVIRONMENT
                        Type of environment. One of (prod|dev|stage) Example:
                        update_site.py -e stage
  -v, --verbose         Echo actions before taking them.
"""

import os
import sys
from textwrap import dedent
from optparse import  OptionParser

# Constants
PROJECT = 0
VENDOR  = 1

ENV_BRANCH = {
    # 'environment': [PROJECT_BRANCH, VENDOR_BRANCH],
    'dev':   ['base',   'master'], 
    'stage': ['master', 'master'], 
    'prod':  ['prod',   'master'],
}

GIT_PULL = "git pull -q origin %(branch)s"
GIT_SUBMODULE = "git submodule update --init"
SVN_UP = "svn update"

EXEC = 'exec'
CHDIR = 'chdir'


def update_site(env, debug):
    """Run through commands to update this site."""
    error_updating = False
    here = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    project_branch = {'branch': ENV_BRANCH[env][PROJECT]}
    vendor_branch = {'branch': ENV_BRANCH[env][VENDOR]}

    commands = [
        (CHDIR, here),
        (EXEC,  GIT_PULL % project_branch),
        (EXEC,  GIT_SUBMODULE),
    ]

    # Update locale dir if applicable
    if os.path.exists(os.path.join(here, 'locale', '.svn')):
        commands += [
            (CHDIR, os.path.join(here, 'locale')),
            (EXEC, SVN_UP),
            (CHDIR, here),
        ]
    elif os.path.exists(os.path.join(here, 'locale', '.git')):
        commands += [
            (CHDIR, os.path.join(here, 'locale')),
            (EXEC, GIT_PULL % 'master'),
            (CHDIR, here),
        ]

    commands += [
        (CHDIR, os.path.join(here, 'vendor')),
        (EXEC,  GIT_PULL % vendor_branch),
        (EXEC,  GIT_SUBMODULE),
        (CHDIR, os.path.join(here)),
        (EXEC, 'python vendor/src/schematic/schematic migrations/'),
        (EXEC, 'python manage.py compress_assets'),
    ]

    for cmd, cmd_args in commands:
        if CHDIR == cmd:
            if debug:
                sys.stdout.write("cd %s\n" % cmd_args)
            os.chdir(cmd_args)
        elif EXEC == cmd:
            if debug:
                sys.stdout.write("%s\n" % cmd_args)
            if not 0 == os.system(cmd_args):
                error_updating = True
                break
        else:
            raise Exception("Unknown type of command %s" % cmd)

    if error_updating:
        sys.stderr.write("There was an error while updating. Please try again "
                         "later. Aborting.\n")


def main():
    """ Handels command line args. """
    debug = False
    usage = dedent("""\
        %prog [options]
        Updates a server's sources, vendor libraries, packages CSS/JS
        assets, migrates the database, and other nifty deployment tasks.
        """.rstrip())

    options = OptionParser(usage=usage)
    e_help = "Type of environment. One of (%s) Example: update_site.py \
        -e stage" % '|'.join(ENV_BRANCH.keys())
    options.add_option("-e", "--environment", help=e_help)
    options.add_option("-v", "--verbose",
                       help="Echo actions before taking them.",
                       action="store_true", dest="verbose")
    (opts, _) = options.parse_args()

    if opts.verbose:
        debug = True
    if opts.environment in ENV_BRANCH.keys():
        update_site(opts.environment, debug)
    else:
        sys.stderr.write("Invalid environment!\n")
        options.print_help(sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
