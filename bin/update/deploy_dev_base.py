import logging

from commander.deploy import task

from deploy_base import *  # noqa


log = logging.getLogger(__name__)


@task
def database(ctx):
    with ctx.lcd(settings.SRC_DIR):
        # only ever run this one on demo and dev.
        ctx.local("python2.6 manage.py bedrock_truncate_database --yes-i-am-sure")
        ctx.local("python2.6 manage.py syncdb --migrate --noinput")
