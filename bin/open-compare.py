#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
import webbrowser


ENV_URLS = {
    'demo1': 'https://www-demo1.allizom.org',
    'demo2': 'https://www-demo2.allizom.org',
    'demo3': 'https://www-demo3.allizom.org',
    'stage': 'https://www.allizom.org',
    'prod': 'https://www.mozilla.org',
}
REV_PATH = '/revision.txt'
DEFAULT_REPO = 'mozilla/bedrock'
DEFAULT_BRANCH = 'master'
URL_TEMPLATE = 'https://github.com/{repo}/compare/{rev}...{branch}'
GITHUB_API_TEMPLATE = 'https://api.github.com/repos/{repo}/branches/{branch}'


def get_current_rev(env):
    url = None
    try:
        url = urllib.request.urlopen(ENV_URLS[env] + REV_PATH)
        return url.read().strip()[:10]
    finally:
        if url:
            url.close()


def get_current_master(repo, branch):
    url = GITHUB_API_TEMPLATE.format(repo=repo, branch=branch)
    conn = None
    try:
        conn = urllib.request.urlopen(url, timeout=30)
        info = json.loads(conn.read().strip())
        return info['commit']['sha'][:10]
    except Exception:
        return branch
    finally:
        if conn:
            conn.close()


def get_compare_url(env, branch=DEFAULT_BRANCH, repo=DEFAULT_REPO):
    rev = get_current_rev(env)
    sha = get_current_master(repo, branch)
    return URL_TEMPLATE.format(rev=rev, branch=sha, repo=repo)


def write_stdout(out_str):
    sys.stdout.write(out_str)
    sys.stdout.flush()


def main():
    parser = argparse.ArgumentParser(description='Open github compare view '
                                                 'for bedrock.')
    parser.add_argument('-e', '--env', default='prod', choices=list(ENV_URLS.keys()),
                        metavar='ENV', help='Environment: demo[1-3], '
                                            'stage, or prod (default)')
    parser.add_argument('-r', '--repo', default=DEFAULT_REPO,
                        help='Repository. Default: ' + DEFAULT_REPO)
    parser.add_argument('-b', '--branch', default=DEFAULT_BRANCH,
                        help='Branch. Default: ' + DEFAULT_BRANCH)
    parser.add_argument('-p', '--print', action='store_true', dest='print_only',
                        help='Just print the URL instead of opening it.')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increase wordiness.')
    args = parser.parse_args()
    args_dict = vars(args).copy()
    del args_dict['verbose']
    del args_dict['print_only']
    if args.verbose:
        out = 'Opening github url for {repo} comparing {env} with {branch}...\n'
        write_stdout(out.format(**args_dict))
    try:
        compare_url = get_compare_url(**args_dict)
        write_stdout(compare_url)
        if not args.print_only:
            webbrowser.open(compare_url)
    except Exception as e:
        sys.stderr.write('\nERROR: {0}\n'.format(e))
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
