"""
Deployment for Bedrock in production.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from commander.deploy import task, hostgroups

import commander_settings as settings


# Functions below called by chief in this order


@task
def pre_update(ctx, ref=settings.UPDATE_REF):
    print "done"


@task
def update(ctx):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local('bin/update-scripts/prod/update-prod-product-details.sh')


@hostgroups(settings.WEB_HOSTGROUP, remote_kwargs={'ssh_key': settings.SSH_KEY})
def deploy(ctx):
    ctx.remote("service httpd graceful")
