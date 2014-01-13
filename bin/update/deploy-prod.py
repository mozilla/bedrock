"""
Deployment for Bedrock on www.mozilla.org.

Requires commander (https://github.com/oremj/commander) which is installed on
the systems that need it.
"""
import os
import sys

# these files are symlinked as 'update.py' in the project root.
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT, 'bedrock', 'bin', 'update'))

from deploy_base import *  # noqa
