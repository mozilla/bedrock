# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import OrderedDict

from bedrock.mozorg import forums
from bedrock.mozorg.tests import TestCase


FORUMS_GOOD_CONTENT = [
    ':Particularly Important Forums\n',
    '\n',
    'mozilla.announce                        New releases will be announced here.\n',
    'mozilla.announce.compatibility          Add-on compatibility announcements. (Moderated)\n',
    '\n',
    ':Applications and Projects\n',
    '\n',
    'firefox-dev                             For development of Firefox.\n',
]

FORUMS_GOOD_DICT = OrderedDict()
FORUMS_GOOD_DICT['Particularly Important Forums'] = [
    {'id': 'mozilla.announce', 'dashed': 'announce',
     'description': 'New releases will be announced here.'},
    {'id': 'mozilla.announce.compatibility', 'dashed': 'announce-compatibility',
     'description': 'Add-on compatibility announcements. (Moderated)'},
]
FORUMS_GOOD_DICT['Applications and Projects'] = [
    {'id': 'firefox-dev', 'dashed': 'firefox-dev', 'description': 'For development of Firefox.'},
]


class TestForums(TestCase):
    def setUp(self):
        self.forums_file = forums.ForumsFile('forums')

    def test_forums_ordered(self):
        """Should give an ordered dict of forums from file."""
        for title, forums_list in list(self.forums_file._parse(FORUMS_GOOD_CONTENT).items()):
            for i, forum in enumerate(forums_list):
                self.assertDictEqual(forum, FORUMS_GOOD_DICT[title][i])

    def test_forums_validation(self):
        with self.assertRaises(ValueError):
            # shouldn't be enough data
            self.forums_file.validate_content(''.join(FORUMS_GOOD_CONTENT))
