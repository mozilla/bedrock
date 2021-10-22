# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from everett.manager import ConfigManager, ConfigurationMissingError
from mock import patch

from bedrock.base import waffle_config
from bedrock.mozorg.tests import TestCase

GOOD_CONFIG = {
    "THE_DUDE": "abides",
    "BOWLING": "true",
}


@patch.object(waffle_config, "get_config_dict", return_value=GOOD_CONFIG)
class TestConfigDBEnv(TestCase):
    def setUp(self):
        self.cdbe = waffle_config.ConfigDBEnv()
        self.config = ConfigManager([self.cdbe])

    def test_db_config(self, gcd_mock):
        self.assertEqual("abides", self.config("the_dude"))
        self.assertEqual("abides", self.config("dude", namespace="the"))
        self.assertTrue(self.config("bowling", parser=bool))
        self.assertTrue(self.config("BOWLING", parser=bool))
        with self.assertRaises(ConfigurationMissingError):
            self.config("donnie")

    def test_db_config_cache(self, gcd_mock):
        self.assertEqual("abides", self.config("the_dude"))
        self.assertEqual("abides", self.config("the_dude"))
        self.assertEqual(gcd_mock.call_count, 1)
        self.cdbe.last_update -= self.cdbe.timeout + 1
        self.assertEqual("abides", self.config("the_dude"))
        self.assertEqual("abides", self.config("the_dude"))
        self.assertEqual(gcd_mock.call_count, 2)


class TestDictOf(TestCase):
    def test_dict_of(self):
        parser = waffle_config.DictOf(int)
        assert parser("dude:1,walter:2,donnie:3") == {
            "dude": 1,
            "walter": 2,
            "donnie": 3,
        }

    def test_dict_of_whitespace(self):
        parser = waffle_config.DictOf(int)
        assert parser(" dude:1, walter: 2 , donnie : 3  ") == {
            "dude": 1,
            "walter": 2,
            "donnie": 3,
        }

    def test_dict_of_floats(self):
        parser = waffle_config.DictOf(float)
        assert parser("dude:1,walter:2,donnie:3.3") == {
            "dude": 1.0,
            "walter": 2.0,
            "donnie": 3.3,
        }

    def test_dict_of_strings(self):
        parser = waffle_config.DictOf(str)
        assert parser("dude:abides,walter:rages,donnie:bowls") == {
            "dude": "abides",
            "walter": "rages",
            "donnie": "bowls",
        }

    def test_wrong_type(self):
        parser = waffle_config.DictOf(int)
        with self.assertRaises(ValueError):
            parser("dude:abides,walter:2,donnie:3")

    def test_empty(self):
        parser = waffle_config.DictOf(int)
        assert parser("") == {}
