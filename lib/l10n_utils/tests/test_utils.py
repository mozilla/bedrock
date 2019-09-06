# coding=utf-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from lib.l10n_utils.utils import ContainsEverything, get_l10n_path


def test_contains_everything():
    all_the_things = ContainsEverything()
    assert 'dude' in all_the_things
    assert 42 in all_the_things
    assert list in all_the_things


def test_get_l10n_path():
    assert get_l10n_path('/apps/foo/templates/foo/bar.html') == 'foo/bar'
    assert get_l10n_path('/templates/foo.html') == 'foo'
    assert get_l10n_path('/foo/bar.html') == 'foo/bar'
