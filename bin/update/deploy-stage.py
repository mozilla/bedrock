"""
Deployment for Bedrock on www.allizom.org.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import os
import sys

from commander.deploy import task

# these files are symlinked as 'update.py' in the project root.
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT, 'bedrock', 'bin', 'update'))

from deploy_base import *  # noqa


@task
def update_cron(ctx):
    generate_cron_file(ctx, 'bedrock-stage')
