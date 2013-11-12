"""
Deployment for Bedrock in production.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import os

from commander.deploy import commands, task, hostgroups

import commander_settings as settings


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

        ctx.local("git rev-parse HEAD > media/revision.txt")


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


@task
def update_bedrock(ctx, tag):
    """Do typical bedrock update"""
    commands['pre_update'](tag)
    commands['update']()
