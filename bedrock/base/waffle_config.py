from time import time

from everett.manager import (
    ConfigDictEnv,
    ConfigEnvFileEnv,
    ConfigManager,
    ConfigOSEnv,
)

from bedrock.base.models import get_config_dict


class ConfigDBEnv(ConfigDictEnv):
    def __init__(self):
        # have to use this directly since settings aren't yet setup
        # when we use this in the settings file
        self._data = None
        self.timeout = 300
        self.last_update = 0

    def get_cache(self):
        if time() > self.last_update + self.timeout:
            return None

        return self._data

    def set_cache(self, data):
        self._data = data
        self.last_update = time()

    @property
    def cfg(self):
        # this is the method called by the get method
        # of the superclass
        configs = self.get_cache()
        if not configs:
            configs = get_config_dict()
            self.set_cache(configs)

        return configs


config = ConfigManager([
    ConfigOSEnv(),
    ConfigEnvFileEnv('.env'),
    ConfigDBEnv(),
])
