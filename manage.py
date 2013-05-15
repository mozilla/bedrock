#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys

# Edit this if necessary or override the variable in your environment.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bedrock.settings')

# Add a temporary path so that we can import the funfactory
tmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'vendor', 'src', 'funfactory')
# Comment out to load funfactory from your site packages instead
sys.path.insert(0, tmp_path)

from funfactory import manage

# Let the path magic happen in setup_environ() !
sys.path.remove(tmp_path)


manage.setup_environ(__file__, more_pythonic=True)

if __name__ == "__main__":
    manage.main()
