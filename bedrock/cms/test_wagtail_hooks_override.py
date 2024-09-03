# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from wagtail import hooks


def test_after_create_page_is_no_longer_in_wagtail_hooks():
    # In bedrock.cms.apps we have code that deliberately disables
    # the `after_create_page` hook added by `wagtail_localize.synctree`
    #
    # This test confirms that it's not there. For now we just ensure
    # there is nothing registered against the `after_create_page`` hook
    # at all. In the future this test may break if other apps (or our own
    # code) add a different function to to `after_create_page`` hook.
    # At that point, this test will need updating to allow for that.

    assert hooks.get_hooks("after_create_page") == []
