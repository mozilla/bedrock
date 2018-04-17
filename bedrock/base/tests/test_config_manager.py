from everett.manager import ConfigManager, ConfigurationMissingError
from mock import Mock

from bedrock.base.config_manager import ConfigDBEnv
from bedrock.mozorg.tests import TestCase


class TestConfigDBEnv(TestCase):
    def setUp(self):
        cdbe = ConfigDBEnv()
        cdbe.conn = Mock()
        cdbe.conn.cursor().execute.return_value = (
            ('THE_DUDE', 'abides'),
            ('BOWLING', 'true'),
        )
        self.cdbe = cdbe
        self.config = ConfigManager([cdbe])

    def test_db_config(self):
        self.assertEqual('abides', self.config('the_dude'))
        self.assertEqual('abides', self.config('dude', namespace='the'))
        self.assertTrue(self.config('bowling', parser=bool))
        self.assertTrue(self.config('BOWLING', parser=bool))
        with self.assertRaises(ConfigurationMissingError):
            self.config('donnie')

    def test_db_config_cache(self):
        exec_mock = self.cdbe.conn.cursor().execute
        config = {
            'THE_DUDE': 'abides',
            'BOWLING': 'true',
        }
        self.assertDictEqual(self.cdbe.get_config_dict(), config)
        self.assertDictEqual(self.cdbe.cfg, config)
        self.assertDictEqual(self.cdbe.cfg, config)
        self.assertEqual(exec_mock.call_count, 2)
        self.cdbe.last_update -= self.cdbe.timeout + 1
        self.assertDictEqual(self.cdbe.cfg, config)
        self.assertDictEqual(self.cdbe.cfg, config)
        self.assertEqual(exec_mock.call_count, 3)
