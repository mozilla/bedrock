#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import sys
import urllib2
import webbrowser


ENV_URLS = {
    'demo1': 'https://www-demo1.allizom.org',
    'demo2': 'https://www-demo2.allizom.org',
    'demo3': 'https://www-demo3.allizom.org',
    'stage': 'https://www.allizom.org',
    'prod': 'https://www.mozilla.org',
}
REV_PATH = '/media/revision.txt'
DEFAULT_REPO = 'mozilla/bedrock'
DEFAULT_BRANCH = 'master'
URL_TEMPLATE = 'https://github.com/{repo}/compare/{rev}...{branch}'


def get_current_rev(env):
    url = None
    try:
        url = urllib2.urlopen(ENV_URLS[env] + REV_PATH)
        return url.read().strip()
    finally:
        if url:
            url.close()


def get_compare_url(env, branch=DEFAULT_BRANCH, repo=DEFAULT_REPO):
    rev = get_current_rev(env)
    return URL_TEMPLATE.format(rev=rev, branch=branch, repo=repo)


def main():
    parser = argparse.ArgumentParser(description='Open github compare view '
                                                 'for bedrock.')
    parser.add_argument('-e', '--env', default='prod', choices=ENV_URLS.keys(),
                        metavar='ENV', help='Environment: demo[1-3], '
                                            'stage, or prod (default)')
    parser.add_argument('-r', '--repo', default=DEFAULT_REPO,
                        help='Repository. Default: ' + DEFAULT_REPO)
    parser.add_argument('-b', '--branch', default=DEFAULT_BRANCH,
                        help='Branch. Default: ' + DEFAULT_BRANCH)
    parser.add_argument('-q', '--quiet', action='store_true', help='Shut up!')
    args = parser.parse_args()
    args_dict = vars(args).copy()
    del args_dict['quiet']
    if not args.quiet:
        out = 'Opening github url for {repo} comparing {env} with {branch}...\n'
        sys.stdout.write(out.format(**args_dict))
        sys.stdout.flush()
    try:
        webbrowser.open(get_compare_url(**args_dict))
    except Exception, e:
        sys.stderr.write('\nERROR: {0}\n'.format(e))
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
