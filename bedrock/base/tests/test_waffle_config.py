from everett.manager import ConfigManager, ConfigurationMissingError
from mock import patch

from bedrock.base import waffle_config
from bedrock.mozorg.tests import TestCase


GOOD_CONFIG = {
    'THE_DUDE': 'abides',
    'BOWLING': 'true',
}


@patch.object(waffle_config, 'get_config_dict',
              return_value=GOOD_CONFIG)
class TestConfigDBEnv(TestCase):
    def setUp(self):
        self.cdbe = waffle_config.ConfigDBEnv()
        self.config = ConfigManager([self.cdbe])

    def test_db_config(self, gcd_mock):
        self.assertEqual('abides', self.config('the_dude'))
        self.assertEqual('abides', self.config('dude', namespace='the'))
        self.assertTrue(self.config('bowling', parser=bool))
        self.assertTrue(self.config('BOWLING', parser=bool))
        with self.assertRaises(ConfigurationMissingError):
            self.config('donnie')

    def test_db_config_cache(self, gcd_mock):
        self.assertEqual('abides', self.config('the_dude'))
        self.assertEqual('abides', self.config('the_dude'))
        self.assertEqual(gcd_mock.call_count, 1)
        self.cdbe.last_update -= self.cdbe.timeout + 1
        self.assertEqual('abides', self.config('the_dude'))
        self.assertEqual('abides', self.config('the_dude'))
        self.assertEqual(gcd_mock.call_count, 2)
