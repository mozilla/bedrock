"""
Deployment for Bedrock in production.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import os
import urllib
import urllib2

from commander.deploy import commands, task, hostgroups

import commander_settings as settings


NEW_RELIC_API_KEY = getattr(settings, 'NEW_RELIC_API_KEY', None)
NEW_RELIC_APP_ID = getattr(settings, 'NEW_RELIC_APP_ID', None)
NEW_RELIC_URL = 'https://rpm.newrelic.com/deployments.xml'
GITHUB_URL = 'https://github.com/mozilla/bedrock/compare/{oldrev}...{newrev}'


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
def update_assets(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("LANG=en_US.UTF-8 python2.6 manage.py compress_assets")
        ctx.local("LANG=en_US.UTF-8 python2.6 manage.py update_product_details")


@task
def database(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("python2.6 manage.py syncdb --migrate --noinput")


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
        #ctx.local("python ./vendor/src/schematic/schematic -v migrations/")
        #ctx.local("python ./manage.py migrate --list")
        with ctx.lcd("locale"):
            ctx.local("svn info")
            ctx.local("svn status")

        ctx.local("mv media/revision.txt media/prev-revision.txt")
        ctx.local("git rev-parse HEAD > media/revision.txt")


@task
def ping_newrelic(ctx):
    if NEW_RELIC_API_KEY and NEW_RELIC_APP_ID:
        with ctx.lcd(settings.SRC_DIR):
            oldrev = ctx.local('cat media/prev-revision.txt').out.strip()
            newrev = ctx.local('cat media/revision.txt').out.strip()

        print 'Post deployment to New Relic'
        data = urllib.urlencode({
            'deployment[description]': 'Chief Deployment',
            'deployment[revision]': newrev,
            'deployment[app_id]': NEW_RELIC_APP_ID,
            'deployment[changelog]': GITHUB_URL.format(oldrev=oldrev,
                                                       newrev=newrev),
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
    commands['database']()


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
