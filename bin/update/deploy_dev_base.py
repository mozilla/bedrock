import logging

from commander.deploy import task

from deploy_base import *  # noqa


log = logging.getLogger(__name__)


@task
def database(ctx):
    # only ever run this one on demo and dev.
    management_cmd(ctx, 'bedrock_truncate_database --yes-i-am-sure')
    management_cmd(ctx, 'syncdb --migrate --noinput')
    management_cmd(ctx, 'rnasync')
    management_cmd(ctx, 'update_security_advisories --force --quiet', use_src_dir=True)
    management_cmd(ctx, 'cron update_reps_ical')
    management_cmd(ctx, 'cron update_tweets')
    management_cmd(ctx, 'runscript update_firefox_os_feeds')
