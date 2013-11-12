"""
Deployment for Bedrock on www-demo2.allizom.org.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import os.path
import sys

from commander.deploy import task

# these files are symlinked as 'update.py' in the project root.
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT, 'bedrock', 'bin', 'update'))

from deploy_dev_base import *  # noqa


@task
def update_code(ctx, tag):
    with ctx.lcd(settings.SRC_DIR):
        ctx.local("git fetch")
        ctx.local("git fetch private")
        ctx.local("git checkout -f %s" % tag)
        ctx.local("git submodule sync")
        ctx.local("git submodule update --init --recursive")
