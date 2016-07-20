# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime

from django.conf import settings

from mock import patch

from bedrock.mozorg.tests import TestCase
from bedrock.tabzilla.views import template_last_modified


@patch('bedrock.tabzilla.views.os.path.getmtime')
@patch('bedrock.tabzilla.views.loader.get_template')
class LastModifiedTests(TestCase):
    def test_youngest_file_wins(self, template_mock, mtime_mock):
        tmpl_name = 'the_dude_is_a_template.html'
        template_mock.return_value.template.filename = tmpl_name
        mtimes = [1378762234.0, 1378762235.0]
        mtime_mock.side_effect = mtimes
        func = template_last_modified(tmpl_name)
        datestamp = func({})
        self.assertEqual(datestamp, datetime.fromtimestamp(max(mtimes)))
        mtime_mock.assert_any_call(tmpl_name)
        langfile = '{0}/locale/en-US/tabzilla/tabzilla.lang'.format(settings.ROOT)
        mtime_mock.assert_any_call(langfile)
