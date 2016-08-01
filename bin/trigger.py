#!/usr/bin/env python
import os
import sys

import requests

URL = os.getenv('URL', ('https://ci.us-west.moz.works/job/bedrock_base_image/'
                        'buildWithParameters?delay=0&token={secret}&'
                        'TAG={tag}&BUILDONLY={buildonly}'))

if len(sys.argv) < 2:
    print('Usage: {} <tag> [buildonly=true|false]'.format(sys.argv[0]))
    sys.exit(0)

SECRET = os.getenv('WEBHOOK_SECRET')
if not SECRET:
    print('Set WEBHOOK_SECRET environment variable')
    sys.exit(1)
TAG = sys.argv[1]

try:
    BUILDONLY = sys.argv[2]
except IndexError:
    BUILDONLY = 'False'

if BUILDONLY.lower() not in ['false', 'true']:
    print('Valid options for BuildOnly are "true" and "false"')
    sys.exit(1)

requests.post(URL.format(secret=SECRET, tag=TAG, buildonly=BUILDONLY))
