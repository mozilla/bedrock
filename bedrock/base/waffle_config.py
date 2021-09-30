from time import time

from everett.manager import (
    ConfigDictEnv,
    ConfigEnvFileEnv,
    ConfigManager,
    ConfigOSEnv,
    get_parser,
)

from bedrock.base.models import get_config_dict


class DictOf:
    """Parser class that returns values as a dict with string keys and values of the chosen type.

    >>> parser = DictOf(int)
    >>> parser('en:10,de:20')
    {'en': 10, 'de': 20}
    """

    def __init__(self, val_parser):
        self.val_parser = val_parser

    def __call__(self, val):
        val = val.strip()
        val_parser = get_parser(self.val_parser)
        out = {}
        if not val:
            return out

        for part in val.split(","):
            k, v = part.split(":")
            out[k.strip()] = val_parser(v.strip())
        return out


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


config = ConfigManager(
    [
        ConfigOSEnv(),
        ConfigEnvFileEnv(".env"),
        ConfigDBEnv(),
    ]
)
