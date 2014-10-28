# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import glob

import chkcrontab_lib as chkcrontab
from funfactory.settings_base import path

from bedrock.mozorg.tests import TestCase


CRONTAB_FILES = glob.glob(path('etc', 'cron.d', '*'))


class TestCrontabFiles(TestCase):
    def test_crontab_files_have_newlines(self):
        """Crontab files should end with newline character."""
        for filename in CRONTAB_FILES:
            with open(filename) as cronfile:
                self.assertTrue(cronfile.read().endswith('\n'),
                                'No newline at end of ' + filename)

    def test_crontab_files_valid(self):
        """Crontab files should pass validation."""
        for filename in CRONTAB_FILES:
            cronlog = chkcrontab.LogCounter()
            return_value = chkcrontab.check_crontab(filename, cronlog)
            self.assertEqual(return_value, 0, 'Problem with ' + filename)
