"""
Deployment for Bedrock in production.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import random
import re
import urllib
import urllib2

from commander.deploy import commands, task, hostgroups

import commander_settings as settings


PYTHON = getattr(settings, 'PYTHON_PATH', 'python2.6')
NEW_RELIC_API_KEY = getattr(settings, 'NEW_RELIC_API_KEY', None)
NEW_RELIC_APP_ID = getattr(settings, 'NEW_RELIC_APP_ID', None)
NEW_RELIC_URL = 'https://rpm.newrelic.com/deployments.xml'
GITHUB_URL = 'https://github.com/mozilla/bedrock/compare/{oldrev}...{newrev}'
CRON_LOG_DIR = '/var/log/bedrock'


# ########## Commands run by chief ##############
# the following 3 tasks are run directly by chief, in order.

@task
def pre_update(ctx, ref=settings.UPDATE_REF):
    commands['update_code'](ref)
    commands['update_info']()


@task
def update(ctx):
    commands['peep_install']()
    commands['update_revision_file']()
    commands['update_assets']()
    # moves files from SRC_DIR to WWW_DIR
    commands['checkin_changes']()
    commands['database']()
    if 'update_cron' in commands:
        commands['update_cron']()
        commands['reload_crond']()


@task
def deploy(ctx):
    commands['deploy_app']()
    commands['ping_newrelic']()


# ########## End Commands run by chief ##############


def management_cmd(ctx, cmd, use_src_dir=False):
    """Run a Django management command correctly."""
    run_dir = settings.SRC_DIR if use_src_dir else settings.WWW_DIR
    with ctx.lcd(run_dir):
        ctx.local('LANG=en_US.UTF-8 {0} manage.py {1}'.format(PYTHON, cmd))


@task
def reload_crond(ctx):
    """Restart cron daemon."""
    ctx.local("killall -SIGHUP crond")


@task
def update_code(ctx, tag):
    """Update the code via git."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("git fetch --all")
        ctx.local("git checkout -f %s" % tag)
        ctx.local("git submodule sync")
        ctx.local("git submodule update --init --recursive")
        ctx.local("find . -name '*.pyc' -delete")


@task
def update_assets(ctx):
    """Compile/compress static assets and fetch external data."""
    management_cmd(ctx, 'collectstatic --noinput', use_src_dir=True)
    management_cmd(ctx, 'update_product_details', use_src_dir=True)
    management_cmd(ctx, 'update_externalfiles', use_src_dir=True)


@task
def update_revision_file(ctx):
    """Add a file containing the current git hash to media."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("if [ -f media/revision.txt ]; then "
                  "mv media/revision.txt media/prev-revision.txt; "
                  "fi")
        ctx.local("git rev-parse HEAD > media/revision.txt")


@task
def database(ctx):
    """Update the database."""
    management_cmd(ctx, 'syncdb --migrate --noinput')


@task
def checkin_changes(ctx):
    """Sync files from SRC_DIR to WWW_DIR ignoring .git"""
    ctx.local(settings.DEPLOY_SCRIPT)


@hostgroups(settings.WEB_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def deploy_app(ctx):
    """Push code to the webheads"""
    ctx.remote(settings.REMOTE_UPDATE_SCRIPT)
#    ctx.remote("/bin/touch %s" % settings.REMOTE_WSGI)
    ctx.remote("service httpd graceful")


@task
def update_info(ctx):
    """Add a bunch of info to the deploy log."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("date")
        ctx.local("git branch")
        ctx.local("git log -3")
        ctx.local("git status")
        ctx.local("git submodule status")
        with ctx.lcd("locale"):
            ctx.local("svn info")
            ctx.local("svn status")


@task
def peep_install(ctx):
    """Install things using peep."""
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('../venv/bin/peep install -r requirements/compiled.txt')


@task
def ping_newrelic(ctx):
    if NEW_RELIC_API_KEY and NEW_RELIC_APP_ID:
        with ctx.lcd(settings.SRC_DIR):
            oldrev = ctx.local('if [ -f media/prev-revision.txt ]; then '
                               'cat media/prev-revision.txt; '
                               'fi').out.strip()
            newrev = ctx.local('if [ -f media/revision.txt ]; then '
                               'cat media/revision.txt; '
                               'fi').out.strip()
            if oldrev and newrev:
                log_cmd = 'git log --oneline {0}..{1}'.format(oldrev, newrev)
                changelog = ctx.local(log_cmd).out.strip()
            else:
                changelog = None

        print 'Post deployment to New Relic'
        desc = generate_desc(oldrev, newrev, changelog)
        if changelog:
            github_url = GITHUB_URL.format(oldrev=oldrev, newrev=newrev)
            changelog = '{0}\n\n{1}'.format(changelog, github_url)
        data = {
            'deployment[description]': desc,
            'deployment[revision]': newrev,
            'deployment[app_id]': NEW_RELIC_APP_ID,
        }
        if changelog:
            data['deployment[changelog]'] = changelog

        data = urllib.urlencode(data)
        headers = {'x-api-key': NEW_RELIC_API_KEY}
        try:
            request = urllib2.Request(NEW_RELIC_URL, data, headers)
            urllib2.urlopen(request)
        except urllib2.URLError as exp:
            print 'Error notifying New Relic: {0}'.format(exp)


@task
def update_bedrock(ctx, tag):
    """Do typical bedrock update"""
    commands['pre_update'](tag)
    commands['update']()


# utility functions #
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


def generate_cron_file(ctx, tmpl_name):
    with ctx.lcd(settings.WWW_DIR):
        ctx.local("{python} bin/gen-crons.py -p {python} -s {src_dir} "
                  "-w {www_dir} -l {log_dir} -t {template}".format(
                      python=PYTHON,
                      src_dir=settings.SRC_DIR,
                      www_dir=settings.WWW_DIR,
                      log_dir=CRON_LOG_DIR,
                      template=tmpl_name))
