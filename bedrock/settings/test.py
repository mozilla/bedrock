# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from bedrock.settings import *  # noqa

# this bypasses bcrypt to speed up test fixtures
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
