# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from nose.tools import ok_

from lib.l10n_utils.utils import ContainsEverything


def test_contains_everything():
    all_the_things = ContainsEverything()
    ok_('dude' in all_the_things)
    ok_(42 in all_the_things)
    ok_(list in all_the_things)
