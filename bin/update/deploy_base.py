"""
Deployment for Bedrock in production.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import os
import random
import re
import urllib
import urllib2

from commander.deploy import commands, task, hostgroups

import commander_settings as settings


NEW_RELIC_API_KEY = getattr(settings, 'NEW_RELIC_API_KEY', None)
NEW_RELIC_APP_ID = getattr(settings, 'NEW_RELIC_APP_ID', None)
NEW_RELIC_URL = 'https://rpm.newrelic.com/deployments.xml'
GITHUB_URL = 'https://github.com/mozilla/bedrock/compare/{oldrev}...{newrev}'


def management_cmd(ctx, cmd):
    """Run a Django management command correctly."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('LANG=en_US.UTF-8 python2.6 manage.py ' + cmd)


@task
def update_code(ctx, tag):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("git fetch")
        ctx.local("git checkout -f %s" % tag)
        ctx.local("git submodule sync")
        ctx.local("git submodule update --init --recursive")


@task
def update_locales(ctx):
    with ctx.lcd(os.path.join(settings.SRC_DIR, 'locale')):
        ctx.local("svn up")


@task
def update_sitemaps(ctx):
    with ctx.lcd(settings.SRC_DIR):
        # lib.sitemaps.management.commands.update_sitemaps()
        ctx.local("LANG=en_US.UTF-8 python2.6 manage.py update_sitemaps")


@task
def update_assets(ctx):
    management_cmd(ctx, 'compress_assets')
    management_cmd(ctx, 'update_product_details')


@task
def update_revision_file(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("mv media/revision.txt media/prev-revision.txt")
        ctx.local("git rev-parse HEAD > media/revision.txt")


@task
def database(ctx):
    management_cmd(ctx, 'syncdb --migrate --noinput')


@task
def checkin_changes(ctx):
    ctx.local(settings.DEPLOY_SCRIPT)


@hostgroups(settings.WEB_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def deploy_app(ctx):
    ctx.remote(settings.REMOTE_UPDATE_SCRIPT)
#    ctx.remote("/bin/touch %s" % settings.REMOTE_WSGI)
    ctx.remote("service httpd graceful")


@task
def update_info(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("date")
        ctx.local("git branch")
        ctx.local("git log -3")
        ctx.local("git status")
        ctx.local("git submodule status")
        with ctx.lcd("locale"):
            ctx.local("svn info")
            ctx.local("svn status")
    management_cmd(ctx, 'migrate --list')


@task
def ping_newrelic(ctx):
    if NEW_RELIC_API_KEY and NEW_RELIC_APP_ID:
        with ctx.lcd(settings.SRC_DIR):
            oldrev = ctx.local('cat media/prev-revision.txt').out.strip()
            newrev = ctx.local('cat media/revision.txt').out.strip()
            log_cmd = 'git log --oneline {0}..{1}'.format(oldrev, newrev)
            changelog = ctx.local(log_cmd).out.strip()

        print 'Post deployment to New Relic'
        desc = generate_desc(oldrev, newrev, changelog)
        if changelog:
            github_url = GITHUB_URL.format(oldrev=oldrev, newrev=newrev)
            changelog = '{0}\n\n{1}'.format(changelog, github_url)
        data = urllib.urlencode({
            'deployment[description]': desc,
            'deployment[revision]': newrev,
            'deployment[app_id]': NEW_RELIC_APP_ID,
            'deployment[changelog]': changelog,
        })
        headers = {'x-api-key': NEW_RELIC_API_KEY}
        try:
            request = urllib2.Request(NEW_RELIC_URL, data, headers)
            urllib2.urlopen(request)
        except urllib.URLError as exp:
            print 'Error notifying New Relic: {0}'.format(exp)


@task
def pre_update(ctx, ref=settings.UPDATE_REF):
    commands['update_code'](ref)
    commands['update_info']()


@task
def update(ctx):
    commands['update_assets']()
    commands['update_locales']()
    commands['update_sitemaps']()
    commands['database']()
    commands['update_revision_file']()


@task
def deploy(ctx):
    commands['checkin_changes']()
    commands['deploy_app']()
    commands['ping_newrelic']()


@task
def update_bedrock(ctx, tag):
    """Do typical bedrock update"""
    commands['pre_update'](tag)
    commands['update']()


## utility functions ##
# shamelessly stolen from https://github.com/mythmon/chief-james/


def get_random_desc():
    return random.choice([
        'No bugfixes--must be adding infinite loops.',
        'No bugfixes--must be rot13ing function names for code security.',
        'No bugfixes--must be demonstrating our elite push technology.',
        'No bugfixes--must be testing james.',
    ])


def extract_bugs(changelog):
    """Takes output from git log --oneline and extracts bug numbers"""
    bug_regexp = re.compile(r'\bbug (\d+)\b', re.I)
    bugs = set()
    for line in changelog:
        for bug in bug_regexp.findall(line):
            bugs.add(bug)

    return sorted(list(bugs))


def generate_desc(from_commit, to_commit, changelog):
    """Figures out a good description based on what we're pushing out."""
    if from_commit.startswith(to_commit):
        desc = 'Pushing {0} again'.format(to_commit)
    else:
        bugs = extract_bugs(changelog.split('\n'))
        if bugs:
            bugs = ['bug #{0}'.format(bug) for bug in bugs]
            desc = 'Fixing: {0}'.format(', '.join(bugs))
        else:
            desc = get_random_desc()
    return desc
