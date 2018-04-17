import sqlite3
from time import time

from everett.manager import (
    ConfigDictEnv,
    ConfigEnvFileEnv,
    ConfigManager,
    ConfigOSEnv,
)


class ConfigDBEnv(ConfigDictEnv):
    def __init__(self):
        # have to use this directly since settings aren't yet setup
        # when we use this in the settings file
        self.conn = sqlite3.connect('bedrock.db')
        self.data = None
        self.timeout = 300
        self.last_update = 0

    def get_cache(self):
        if time() > self.last_update + self.timeout:
            return None

        return self.data

    def set_cache(self, data):
        self.data = data
        self.last_update = time()

    def get_config_dict(self):
        c = self.conn.cursor()
        return dict(c.execute('SELECT name, value FROM base_configvalue'))

    @property
    def cfg(self):
        configs = self.get_cache()
        if not configs:
            configs = self.get_config_dict()
            self.set_cache(configs)

        return configs


config = ConfigManager([
    ConfigOSEnv(),
    ConfigEnvFileEnv('.env'),
    ConfigDBEnv(),
])
