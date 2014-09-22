# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from nose.tools import eq_
from bedrock.mozorg.tests import TestCase
from bedrock.security.management.commands import update_security_advisories


class TestUpdateSecurityAdvisories(TestCase):
    def test_fix_product_name(self):
        """Should fix SeaMonkey and strip '.0' from names."""
        eq_(update_security_advisories.fix_product_name('Seamonkey 2.2'),
            'SeaMonkey 2.2')
        eq_(update_security_advisories.fix_product_name('Firefox 2.2'),
            'Firefox 2.2')
        eq_(update_security_advisories.fix_product_name('fredflintstone 2.2'),
            'fredflintstone 2.2')
        eq_(update_security_advisories.fix_product_name('Firefox 32.0'),
            'Firefox 32')
        eq_(update_security_advisories.fix_product_name('Firefox 32.0.1'),
            'Firefox 32.0.1')
