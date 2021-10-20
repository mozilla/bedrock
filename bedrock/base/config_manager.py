# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from everett.manager import ConfigEnvFileEnv, ConfigManager, ConfigOSEnv

config = ConfigManager(
    [
        # first check for environment variables
        ConfigOSEnv(),
        # then look in the .env file
        ConfigEnvFileEnv(".env"),
    ]
)
